
def _res_to_dpi(num: int, denom: int, exp: int) -> float | None:
    """Convert JPEG2000's (numerator, denominator, exponent-base-10) resolution,
    calculated as (num / denom) * 10^exp and stored in dots per meter,
    to floating-point dots per inch."""
    if denom == 0:
        return None
    return (254 * num * (10**exp)) / (10000 * denom)

