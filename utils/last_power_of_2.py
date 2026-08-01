
def last_power_of_2(n: int) -> int:
    """Return the largest power of 2 less than or equal to n"""
    next_pow2 = next_power_of_2(n)
    return next_pow2 // 2 if next_pow2 > n else next_pow2

