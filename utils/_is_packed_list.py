from typing import Any

def _is_packed_list(list_value: Any) -> bool:
    return _is_value(list_value) and list_value.node().kind() == "prim::ListConstruct"

