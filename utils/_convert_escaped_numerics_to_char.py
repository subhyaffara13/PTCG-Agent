
def _convert_escaped_numerics_to_char(s: str) -> str:
    if s == "0":
        return "\0"
    if s.isdigit() and len(s) == 3:
        return chr(int(s, 8))
    elif s.startswith(("u", "x")):
        return chr(int(s[1:], 16))
    return s

