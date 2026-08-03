import os
from typing import Optional

def _get_env_variable(key: str) -> Optional[str]:
    env_prefix = "opik_"
    return os.getenv((env_prefix + key).upper(), None)

