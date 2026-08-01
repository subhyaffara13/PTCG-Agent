
def _div_monom(monom: Iterable[int], div: Iterable[int]) -> tuple[int, ...]:
    return tuple(mi - di for mi, di in zip(monom, div))

