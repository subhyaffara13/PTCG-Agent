from typing import Any

def vertical_grid(**interface: Any) -> str:
    return _vertical_grid_common(need_trailing_char=True, **interface) + ")"

