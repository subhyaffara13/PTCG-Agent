import sys
from typing import Any

def default_ignored_types() -> tuple[type[Any], ...]:
    from ..fields import ComputedFieldInfo

    ignored_types = [
        FunctionType,
        property,
        classmethod,
        staticmethod,
        PydanticDescriptorProxy,
        ComputedFieldInfo,
        TypeAliasType,  # from `typing_extensions`
    ]

    if sys.version_info >= (3, 12):
        ignored_types.append(typing.TypeAliasType)

    return tuple(ignored_types)

