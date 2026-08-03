import sys
from typing import Any, Optional, Union

def is_union(ann):
    if ann is Union:
        raise_error_container_parameter_missing("Union")

    return isinstance(ann, BuiltinUnionType) or (
        hasattr(ann, "__module__")
        and ann.__module__ == "typing"
        and (get_origin(ann) is Union)
    )


def is_union(tp: type[Any] | None) -> bool:
    return tp is Union or tp is types.UnionType  # noqa: E721


def is_union(tp: Optional[Type[Any]]) -> bool:
    if sys.version_info < (3, 10):
        return tp is Union  # type: ignore[comparison-overlap]
    else:
        import types

        return tp is Union or tp is types.UnionType  # type: ignore[comparison-overlap]

