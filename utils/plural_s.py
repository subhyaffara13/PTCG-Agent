
def plural_s(s: int | Sized) -> str:
    count = s if isinstance(s, int) else len(s)
    if count != 1:
        return "s"
    else:
        return ""

