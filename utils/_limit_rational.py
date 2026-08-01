
def _limit_rational(
    val: float | Fraction | IFDRational, max_val: int
) -> tuple[IntegralLike, IntegralLike]:
    inv = abs(val) > 1
    n_d = IFDRational(1 / val if inv else val).limit_rational(max_val)
    return n_d[::-1] if inv else n_d

