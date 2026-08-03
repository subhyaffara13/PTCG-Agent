from typing import Any

def is_finalvar(ann_type: Type[Any]) -> bool:
    return _check_finalvar(ann_type) or _check_finalvar(get_origin(ann_type))


def is_finalvar(tp: Any, /) -> bool:
    """Return whether the provided argument is a `Final` special form, parametrized or not.

    ```python {test="skip" lint="skip"}
    is_finalvar(Final[int])
    #> True
    is_finalvar(Final)
    #> True
    """
    # Final is not necessarily parametrized:
    if tp is _t_final or tp is _te_final:
        return True
    origin = get_origin(tp)
    return origin is _t_final or origin is _te_final

