
def get_base64_str(s: str) -> str:
    """
    s: b64str OR data:image/png;base64,b64str
    """
    if "," in s:
        return s.split(",")[1]
    return s

