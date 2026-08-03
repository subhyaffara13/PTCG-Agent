from typing import Any

def is_annotated(tp: Any, /) -> bool:
    """Return whether the provided argument is a `Annotated` special form.

    ```python {test="skip" lint="skip"}
    is_annotated(Annotated[int, ...])
    #> True
    ```
    """
    origin = get_origin(tp)
    return origin is _t_annotated or origin is _te_annotated

