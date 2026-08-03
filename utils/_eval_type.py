import sys
from typing import Any

def _eval_type(
    value: Any,
    globalns: GlobalsNamespace | None = None,
    localns: MappingNamespace | None = None,
    type_params: tuple[Any, ...] | None = None,
) -> Any:
    if sys.version_info >= (3, 14):
        # Starting in 3.14, `_eval_type()` does *not* apply `_type_convert()`
        # anymore. This means the `None` -> `type(None)` conversion does not apply:
        evaluated = typing._eval_type(  # type: ignore
            value,
            globalns,
            localns,
            type_params=type_params,
            # This is relevant when evaluating types from `TypedDict` classes, where string annotations
            # are automatically converted to `ForwardRef` instances with a module set. In this case,
            # Our `globalns` is irrelevant and we need to indicate `typing._eval_type()` that it should
            # infer it from the `ForwardRef.__forward_module__` attribute instead (`typing.get_type_hints()`
            # does the same). Note that this would probably be unnecessary if we properly iterated over the
            # `__orig_bases__` for TypedDicts in `get_cls_type_hints()`:
            prefer_fwd_module=True,
        )
        if evaluated is None:
            evaluated = type(None)
        return evaluated
    elif sys.version_info >= (3, 13):
        return typing._eval_type(  # type: ignore
            value, globalns, localns, type_params=type_params
        )
    else:
        return typing._eval_type(  # type: ignore
            value, globalns, localns
        )

