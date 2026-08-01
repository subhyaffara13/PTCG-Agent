
def _unicode_escape(seq: str) -> str:
    return "".join(f"\\u{ord(c):04x}" for c in seq)

