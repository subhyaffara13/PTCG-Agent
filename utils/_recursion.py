from typing import Any

def _recursion(object: Any) -> str:
    return f"<Recursion on {type(object).__name__} with id={id(object)}>"

