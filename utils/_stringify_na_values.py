
def _stringify_na_values(na_values, floatify: bool) -> set[str | float]:
    """return a stringified and numeric for these values"""
    result: list[str | float] = []
    for x in na_values:
        result.append(str(x))
        result.append(x)
        try:
            v = float(x)

            # we are like 999 here
            if v == int(v):
                v = int(v)
                result.append(f"{v}.0")
                result.append(str(v))

            if floatify:
                result.append(v)
        except (TypeError, ValueError, OverflowError):
            pass
        if floatify:
            try:
                result.append(int(x))
            except (TypeError, ValueError, OverflowError):
                pass
    return set(result)

