
def iszero(mpf: MPF_TUP | SCALED_ZERO_TUP | None, scaled=False) -> bool | None:
    if not scaled:
        return not mpf or not mpf[1] and not mpf[-1]
    return mpf and isinstance(mpf[0], list) and mpf[1] == mpf[-1] == 1

