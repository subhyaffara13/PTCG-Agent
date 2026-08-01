
def is_power_of_2(n: int) -> bool:
    """Returns whether n = 2 ** m for some integer m."""
    return n > 0 and n & n - 1 == 0


def is_power_of_2(n):
    return n != 0 and ((n & (n - 1)) == 0)

