
def RubikGroup(n):
    """Return a group of Rubik's cube generators

    >>> from sympy.combinatorics.named_groups import RubikGroup
    >>> RubikGroup(2).is_group
    True
    """
    from sympy.combinatorics.generators import rubik
    if n <= 1:
        raise ValueError("Invalid cube. n has to be greater than 1")
    return PermutationGroup(rubik(n))

