import os
from typing import Dict, List

import requests

from interfaces.base import BaseInterface
from utils import should_have_all_defined


class LLAMA2Interface(BaseInterface):
    def __init__(self, context: str, prompts: Dict[str, str], max_tokens: int = 40000, temperature: float = 0):
        should_have_all_defined(["LLAMA2_API_URL"])

        self.ngrok_url = os.environ["LLAMA2_API_URL"]

        self.evaluations = [
            {
                "title": "Grammar",
                "description": "Grammar suggestions for your text.",
                "method": self.evaluate_prompts_by_grammar,
            },
            {
                "title": "Theme",
                "description": "Theme suggestions for your text.",
                "method": self.evaluate_prompts_by_theme,
            },
        ]

        super().__init__(
            context=context,
            prompts=prompts,
            model=None,
            evaluations=self.evaluations,
            max_tokens=max_tokens,
            temperature=temperature,
        )

    def validate_initialization(self) -> None:
        if not requests.get(self.ngrok_url).ok:
            raise ValueError("Ngrok is not running. Please, run it and try again.")

    def evaluate_prompt_by_theme(self, prompt: str) -> Dict[str, str]:
        input = f"""
            [Context]: You are a scientific article revisor and you are a specialist in every 
            theme that is written in the text.
            Judge with knowledge suggesting the author in which topics he would emphasize 
            better and what should he rewrite to bring better readability of the theme.
            The categories of suggestions are:
            - Improve References;
            - Theme Violation;
            - Missing Related Works if exists;
            - Missing information;
            - Confusing Explanation;
            - Missing Limitations;
            - Others.
            Where the Others you can generate other categories.
            Also use clear language when you are suggesting to be clear in which parts of the 
            text the author should make the changes.
            List as many suggestions as you can.
            The user is also giving you a context about the article, so you can use it
            to evaluate the text: {self.context}

            ---
            {prompt}
        """

        return requests.post(
            self.ngrok_url + "/generate",
            json={
                "inputs": input,
                "parameters": {
                    "temperature": self.temperature,
                    "max_tokens": self.max_tokens,
                    "top_p": 0.5,
                    "frequency_penalty": 0,
                    "presence_penalty": 0,
                },
            },
        ).json()['generated_text']

    def evaluate_prompt_by_grammar(self, prompt: str) -> Dict[str, str]:
        input = f"""
            [Context]: You are a scientific article revisor and one of the steps is the 
            grammar suggestion tool, giving which word or sentence should I change. Besides, 
            check if the document follows the DoCO, the Document Components Ontology that 
            provides a structured vocabulary written in OWL 2 DL of document components, both 
            structural (e.g. block, inline, paragraph, section, chapter) and rhetorical (e.g. 
            introduction, discussion, acknowledgements, reference list, figure, appendix), 
            enabling these components, and documents composed of them, to be described in RDF.
            The user is also giving you a context about the article, so you can use it
            to evaluate the text: {self.context}

            --- 
            Example 1:
            [example input]: IoT software systems have made great strides since the new 
            industrial revolution known as Industry 4.0. Its usage has been growing over the 
            years, and research reports indicate the occurrence of exponential growth related 
            to the utilization of these devices, with a forecast of surpassing 30 billion 
            devices by 2024.
            [your output]: 2 additional writing issues. 1 Unclear sentences. 1 Passive voice 
            misuse. 
            - You should remove "known as" in the sentence: "[...] revolution, known as 
            Industry 4.0. [...]"
            - You should remove "in which it was" in the sentence: "[...] systems in which it 
            was applied and the approach [...]"
            ---
            
            [user input]: This is my prompt: {prompt}
        """
        return requests.post(
            self.ngrok_url + "/generate",
            json={
                "inputs": input,
                "parameters": {
                    "temperature": self.temperature,
                    "max_tokens": self.max_tokens,
                    "top_p": 0.5,
                    "frequency_penalty": 0,
                    "presence_penalty": 0,
                },
            },
        ).json()['generated_text']

    def evaluate_prompts_by_theme(self) -> Dict[str, str]:
        results = {}
        for prompt_name, prompt_text in self.prompts.items():
            result = self.evaluate_prompt_by_theme(prompt_text)
            results[prompt_name] = result
        return results

    def evaluate_prompts_by_grammar(self) -> Dict[str, str]:
        results = {}
        for prompt_name, prompt_text in self.prompts.items():
            result = self.evaluate_prompt_by_grammar(prompt_text)
            results[prompt_name] = result
        return results