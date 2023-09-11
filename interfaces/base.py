from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional


class BaseInterface(ABC):
    def __init__(
        self,
        context: str,
        prompts: Dict[str, str],
        model: Optional[str],
        evaluations: List[Dict[str, Any]],
        max_tokens: int = 10000,
        temperature: float = 0.5,
    ):
        self.context = context
        self.prompts = prompts
        self.model = model
        self.max_tokens = max_tokens
        self.temperature = temperature
        self.evaluations = evaluations
        self.response = self.get_response()

    @abstractmethod
    def validate_initialization(self):
        pass

    def get_response(self) -> Dict[str, Dict[str, str]]:
        self.validate_initialization()

        # Execute each evaluation method and store the results
        evaluation_results = {}
        for evaluation in self.evaluations:
            evaluation_results[evaluation["title"]] = evaluation["method"]()

        return evaluation_results
