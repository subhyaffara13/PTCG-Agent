
def find_carmichael_numbers_in_range(x, y):
    """ Returns a list of the number of Carmichael in the range

    See Also
    ========

    is_carmichael

    """
    if 0 <= x <= y:
        if x % 2 == 0:
            return [i for i in range(x + 1, y, 2) if is_carmichael(i)]
        else:
            return [i for i in range(x, y, 2) if is_carmichael(i)]
    else:
        raise ValueError('The provided range is not valid. x and y must be non-negative integers and x <= y')

