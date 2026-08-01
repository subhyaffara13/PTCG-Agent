
def _c(code: str, text: str) -> str:
    return f"{code}{text}{_RESET}" if _supports_color() else text

