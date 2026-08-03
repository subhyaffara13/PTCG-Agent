from typing import Any

def is_type_alias_type(tp: Any, /) -> TypeIs[typing_extensions.TypeAliasType]:
    """Return whether the provided argument is an instance of `TypeAliasType`.

    ```python
    type Int = int
    is_type_alias_type(Int)
    # > True
    Str = TypeAliasType("Str", str)
    is_type_alias_type(Str)
    # > True
    ```
    """
    return isinstance(tp, _TYPE_ALIAS_TYPES)

