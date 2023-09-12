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
            You are a scientific article reviewer tasked with summarizing a given text.
            <</SYS>>

            Summarize the following text: {text}

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
        ).json()["generated_text"]

    def evaluate_prompt_by_theme(self, prompt: str) -> Dict[str, str]:
        input = f"""[INST] <<SYS>>
            As a scientific article reviewer with expertise in various themes, your role 
            is to provide valuable feedback to the author for better emphasis and 
            readability of the text. Your suggestions may fall into categories such as:
            
            - Improve References
            - Address Theme Violations
            - Identify Missing Related Works (if any)
            - Point Out Missing Information
            - Clarify Confusing Explanations
            - Address Missing Limitations
            - Suggest Other Improvements
            
            You can also create additional categories if needed. Ensure that your feedback 
            is clear and specific, indicating the sections of the text that require changes.

            Utilize the context provided by the user to evaluate the article effectively.
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
        ).json()["generated_text"]

    def evaluate_prompt_by_grammar(self, prompt: str) -> Dict[str, str]:
        input = f"""[INST] <<SYS>>
            You are a scientific article reviewer tasked with grammar suggestions. 
            Additionally, check if the document follows DoCO, the Document Components 
            Ontology, which provides a structured vocabulary for document components, both 
            structural (e.g., block, inline, paragraph, section) and rhetorical (e.g., 
            introduction, discussion, acknowledgments, reference list). This ontology 
            enables these components and documents composed of them to be described in RDF.

            The user has also provided you with context about the article, which you can 
            use to evaluate the text effectively: {self.context}
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
        ).json()["generated_text"]

    def evaluate_prompt_by_cohesion(self) -> Dict[str, str]:
        abstract = self.__summarize_text(self.prompts["abstract"])
        introduction = self.__summarize_text(self.prompts["introduction"])
        conclusion = self.__summarize_text(self.prompts["conclusion"])

        input = f"""[INST] <<SYS>>
            You are a scientific article reviewer tasked with evaluating the coherence 
            between the sections of the provided article. Your role is to assess whether 
            the "Abstract," "Introduction," and "Conclusion" align in terms of their 
            content and messaging. If there are inconsistencies, please provide feedback 
            to the user.

            Your objective is to determine if these sections make sense together. For 
            instance, if the abstract discusses one topic, but the introduction talks 
            about something entirely different, please flag this as a potential issue. 
            Similarly, if the introduction and conclusion have opposing statements, point 
            that out. And if the three sections are consistent, acknowledge their 
            cohesion.

            The user has also provided you with context about the article, which you can 
            use to evaluate the text effectively: {self.context}
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
        ).json()["generated_text"]

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
