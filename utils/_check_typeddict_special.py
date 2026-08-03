from typing import Any

def _check_typeddict_special(type_: Any) -> bool:
    return type_ is TypedDictRequired or type_ is TypedDictNotRequired

