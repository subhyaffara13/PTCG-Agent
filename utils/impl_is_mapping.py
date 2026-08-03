from typing import Any

def impl_IS_MAPPING(a: object) -> TypeIs[Mapping[Any, Any]]:
    return isinstance(a, Mapping)

