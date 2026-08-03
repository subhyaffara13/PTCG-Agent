from typing import Any

def unwrap_if_wrapper(fn: Any) -> Any:
    return unwrap_with_attr_name_if_wrapper(fn)[0]

