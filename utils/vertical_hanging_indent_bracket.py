from typing import Any

def vertical_hanging_indent_bracket(**interface: Any) -> str:
    if not interface["imports"]:
        return ""
    statement = vertical_hanging_indent(**interface)
    return f"{statement[:-1]}{interface['indent']})"

