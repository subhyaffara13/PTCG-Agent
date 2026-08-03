from typing import Any, Callable, Optional

def validate_custom_validate_return_type(
    fn: Optional[Callable[..., Any]],
) -> Optional[Callable[..., Literal[True]]]:
    if fn is None:
        return None

    hints = get_type_hints(fn)
    return_type = hints.get("return")

    if return_type != Literal[True]:
        raise TypeError(
            f"Custom validator must be annotated to return Literal[True], got {return_type}"
        )

    return fn

