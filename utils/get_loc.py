
def get_loc(filename: str, lineno: int) -> str | None:
    try:
        with open(filename) as f:
            for i, line in enumerate(f):
                if i == lineno - 1:
                    return line.strip()
    except FileNotFoundError:
        pass
    return None

