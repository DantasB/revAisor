import os
from typing import Dict

import requests

from interfaces.base import BaseInterface
from utils import should_have_all_defined


class LLAMA2Interface(BaseInterface):
    def __init__(
        self, context: str, prompts: Dict[str, str], max_tokens: int = 10000, temperature: float = 0
    ):
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
            {
                "title": "Cohesion",
                "description": "Evaluate the text by cohesion.",
                "method": self.evaluate_prompt_by_cohesion,
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
    
    def __summarize_text(self, text: str) -> str:
        input = f"""[INST] <<SYS>>
            You are a scientific article revisor and one of the steps is 
            to summarize the text. The user will give you the text and your objective is
            to summarize it.
            <</SYS>>
            summarize this text for me. {text}
            [/INST]
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

    def evaluate_prompt_by_theme(self, prompt: str) -> Dict[str, str]:
        input = f"""[INST] <<SYS>>
            You are a scientific article revisor and you are a specialist in every 
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
            <</SYS>>
            {prompt}
            [/INST]
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
        input = f"""[INST] <<SYS>>
            You are a scientific article revisor and one of the steps is the 
            grammar suggestion tool, giving which word or sentence should I change. Besides, 
            check if the document follows the DoCO, the Document Components Ontology that 
            provides a structured vocabulary written in OWL 2 DL of document components, both 
            structural (e.g. block, inline, paragraph, section, chapter) and rhetorical (e.g. 
            introduction, discussion, acknowledgements, reference list, figure, appendix), 
            enabling these components, and documents composed of them, to be described in RDF.
            The user is also giving you a context about the article, so you can use it
            to evaluate the text: {self.context}
            <</SYS>>        
            {prompt}
            [/INST]
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

    def evaluate_prompt_by_cohesion(self) -> Dict[str, str]:
        abstract = self.__summarize_text(self.prompts['abstract'])
        introduction = self.__summarize_text(self.prompts['introduction'])
        conclusion = self.__summarize_text(self.prompts['conclusion'])

        input = f"""[INST] <<SYS>>
            You are a scientific article revisor and one of the steps is 
            to evaluate the prompt coesion. The user will give you the introduction,
            the abstract and the conclusion of the article. Your objective is to evaluate
            if they make sense, for example, if the user give the abstract and the
            introduction talks about other thing, there's something wrong and you should
            point that to the user. If the introduction says about something but the
            conclusion is the oposite you should also point that to the user. If the 
            introduction and conclusion are consistent but the abstract is not consistent,
            you should also point that to the user. But, if the three are consistents,
            you should say that the three are consistent. The user is also giving you a
            context about the article, so you can use it to evaluate the
            text: {self.context}
            <</SYS>>
            Abstract:{abstract}
            Introduction:{introduction}
            Conclusion:{conclusion}
            [/INST]
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
        return results  # type: ignore

    def evaluate_prompts_by_grammar(self) -> Dict[str, str]:
        results = {}
        for prompt_name, prompt_text in self.prompts.items():
            result = self.evaluate_prompt_by_grammar(prompt_text)
            results[prompt_name] = result
        return results  # type: ignore
