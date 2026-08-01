
def _limit_signed_rational(
    val: IFDRational, max_val: int, min_val: int
) -> tuple[IntegralLike, IntegralLike]:
    frac = Fraction(val)
    n_d: tuple[IntegralLike, IntegralLike] = frac.numerator, frac.denominator

    if min(float(i) for i in n_d) < min_val:
        n_d = _limit_rational(val, abs(min_val))

    n_d_float = tuple(float(i) for i in n_d)
    if max(n_d_float) > max_val:
        n_d = _limit_rational(n_d_float[0] / n_d_float[1], max_val)

    return n_d

