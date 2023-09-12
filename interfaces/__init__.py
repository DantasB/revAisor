from collections import defaultdict

from interfaces.gpt.interface import GPTInterface
from interfaces.llama2.interface import LLAMA2Interface

AVAILABLE_MODELS = defaultdict(
    int, {"GPT-3.5": GPTInterface, "LLAMA2": LLAMA2Interface}  # type: ignore
)
