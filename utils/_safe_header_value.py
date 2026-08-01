
def _safe_header_value(value: str) -> str:
    if not value:
        return ""
    return "".join(ch if 32 <= ord(ch) <= 126 else "_" for ch in value)

