from typing import Any

def is_none_type(type_: Any) -> bool:
    for none_type in NONE_TYPES:
        if type_ is none_type:
            return True
    return False


def is_none_type(tp: Any, /) -> bool:
    """Return whether the argument represents the `None` type as part of an annotation.

    ```python {test="skip" lint="skip"}
    is_none_type(None)
    #> True
    is_none_type(NoneType)
    #> True
    is_none_type(Literal[None])
    #> True
    is_none_type(type[None])
    #> False
    """
    return tp in _NONE_TYPES

