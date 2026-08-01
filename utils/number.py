
def number(s: Any) -> float:
    try:
        return int(s)
    except ValueError:
        return float(s)

