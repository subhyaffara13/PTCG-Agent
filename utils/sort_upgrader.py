from typing import Any

def sort_upgrader(upgrader_list: list[dict[str, Any]]) -> list[dict[str, Any]]:
    sorted_upgrader_list = sorted(
        upgrader_list, key=lambda one_upgrader: next(iter(one_upgrader))
    )
    return sorted_upgrader_list

