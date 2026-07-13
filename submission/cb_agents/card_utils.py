from typing import Any


def _get_prize_yield(card_name: str) -> int:
    if not card_name:
        return 1
    n = card_name.lower()
    if "vmax" in n:
        return 3
    if "vstar" in n or n.endswith(" v") or n.endswith(" ex") or " ex " in n or " v " in n:
        return 2
    return 1


def _int_or_str(val: Any) -> Any:
    try:
        return int(val)
    except Exception:
        return val
