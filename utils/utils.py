from typing import List
import os
from dotenv import load_dotenv

load_dotenv()


def should_have_all_defined(variables: List[str]):
    for env in variables:
        if not os.getenv(env):
            raise ValueError(f"Env Variable {env} not defined.")
