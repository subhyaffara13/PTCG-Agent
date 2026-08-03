from typing import Any

def _manual_list_update(list_from: list[Any], list_to: list[Any]) -> None:
    list.clear(list_to)
    list.extend(list_to, list_from)

