
def n_to_data(n):
    """Convert an integer to one-, four- or eight-unit graph6 sequence.

    This function is undefined if `n` is not in ``range(2 ** 36)``.

    """
    if n <= 62:
        return [n]
    elif n <= 258047:
        return [63, (n >> 12) & 0x3F, (n >> 6) & 0x3F, n & 0x3F]
    else:  # if n <= 68719476735:
        return [
            63,
            63,
            (n >> 30) & 0x3F,
            (n >> 24) & 0x3F,
            (n >> 18) & 0x3F,
            (n >> 12) & 0x3F,
            (n >> 6) & 0x3F,
            n & 0x3F,
        ]

