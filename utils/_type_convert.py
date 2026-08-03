from typing import Any

def _type_convert(arg: Any) -> Any:
    """Convert `None` to `NoneType` and strings to `ForwardRef` instances.

    This is a backport of the private `typing._type_convert` function. When
    evaluating a type, `ForwardRef._evaluate` ends up being called, and is
    responsible for making this conversion. However, we still have to apply
    it for the first argument passed to our type evaluation functions, similarly
    to the `typing.get_type_hints` function.
    """
    if arg is None:
        return NoneType
    if isinstance(arg, str):
        # Like `typing.get_type_hints`, assume the arg can be in any context,
        # hence the proper `is_argument` and `is_class` args:
        return _make_forward_ref(arg, is_argument=False, is_class=True)
    return arg

