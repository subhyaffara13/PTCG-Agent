
def find_first_n_carmichaels(n):
    """ Returns the first n Carmichael numbers.

    Parameters
    ==========

    n : Integer

    See Also
    ========

    is_carmichael

    """
    i = 561
    carmichaels = []

    while len(carmichaels) < n:
        if is_carmichael(i):
            carmichaels.append(i)
        i += 2

    return carmichaels

