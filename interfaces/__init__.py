from interfaces.gpt.interface import GPTInterface
from interfaces.llama2.interface import LLAMA2Interface
from collections import defaultdict

AVAILABLE_MODELS = defaultdict(
    int, {"Modelo 2": GPTInterface, "Modelo 1": LLAMA2Interface}  # type: ignore
)
