
def int_to_int8(n):
    """
    Wrap an integer to the interval [-128, 127].
    """
    return (n + 128) % 256 - 128

