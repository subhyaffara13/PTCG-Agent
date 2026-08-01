
def strip_comment(code: str) -> str:
    return re.sub(r"(?m)^ *#.*\n?", "", code)

