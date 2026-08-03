from typing import Any

def inner_fake(*args: Any, **kwargs: Any) -> None:
    raise RuntimeError("This op should never be invoked here")

