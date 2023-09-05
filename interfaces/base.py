from dotenv import load_dotenv
from abc import ABC, abstractmethod

load_dotenv()

class BaseInterface(ABC):
    def __init__(self, prompt, model, evaluations, max_tokens=10000, temperature=0.5):
        self.prompt = prompt
        self.model = model
        self.max_tokens = max_tokens
        self.temperature = temperature
        self.evaluations = evaluations
        self.response = self.get_response()


    @abstractmethod
    def evaluate_prompt_by_theme(self):
        pass

    @abstractmethod
    def evaluate_prompt_grammar(self):
        pass

    @abstractmethod
    def validate_initialization(self):
        pass

    def get_response(self):
        self.validate_initialization()

        # Execute each evaluation method and store the results
        evaluation_results = {}
        for evaluation in self.evaluations:
            evaluation_results[evaluation["title"]] = evaluation["method"]()

        return {
            "evaluations": evaluation_results
        }
