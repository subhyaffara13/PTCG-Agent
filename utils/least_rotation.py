
def least_rotation(x, key=None):
    '''
    Returns the number of steps of left rotation required to
    obtain lexicographically minimal string/list/tuple, etc.

    Examples
    ========

    >>> from sympy.utilities.iterables import least_rotation, rotate_left
    >>> a = [3, 1, 5, 1, 2]
    >>> least_rotation(a)
    3
    >>> rotate_left(a, _)
    [1, 2, 3, 1, 5]

    References
    ==========

    .. [1] https://en.wikipedia.org/wiki/Lexicographically_minimal_string_rotation

    '''
    from sympy.functions.elementary.miscellaneous import Id
    if key is None: key = Id
    S = x + x      # Concatenate string to it self to avoid modular arithmetic
    f = [-1] * len(S)     # Failure function
    k = 0       # Least rotation of string found so far
    for j in range(1,len(S)):
        sj = S[j]
        i = f[j-k-1]
        while i != -1 and sj != S[k+i+1]:
            if key(sj) < key(S[k+i+1]):
                k = j-i-1
            i = f[i]
        if sj != S[k+i+1]:
            if key(sj) < key(S[k]):
                k = j
            f[j-k] = -1
        else:
            f[j-k] = i+1
    return k

