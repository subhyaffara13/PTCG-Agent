from typing import Any

def _check_is_function_def(obj: Any) -> None:
    if not isinstance(obj, nodes.FunctionDef):
        raise ValueError

