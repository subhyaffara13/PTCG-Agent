
def get_factors(dividend: int) -> set[int]:
    """
    Calculate all factors of a given number, i.e. a divisor that leaves
    no remainder. For example, if dividend=12, it will return {1, 2, 3, 4, 6, 12}.

    Args:
        dividend (int): The number to find factors for.

    Returns:
        set: A set containing all factors of the number.
    """
    factors_set = set()

    for i in range(1, int(dividend**0.5) + 1):
        if dividend % i == 0:
            factors_set.add(i)
            factors_set.add(dividend // i)
    return factors_set

