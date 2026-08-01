
def _orbits(degree, generators):
    """Compute the orbits of G.

    If ``rep=False`` it returns a list of sets else it returns a list of
    representatives of the orbits

    Examples
    ========

    >>> from sympy.combinatorics import Permutation
    >>> from sympy.combinatorics.perm_groups import _orbits
    >>> a = Permutation([0, 2, 1])
    >>> b = Permutation([1, 0, 2])
    >>> _orbits(a.size, [a, b])
    [{0, 1, 2}]
    """

    orbs = []
    sorted_I = list(range(degree))
    I = set(sorted_I)
    while I:
        i = sorted_I[0]
        orb = _orbit(degree, generators, i)
        orbs.append(orb)
        # remove all indices that are in this orbit
        I -= orb
        sorted_I = [i for i in sorted_I if i not in orb]
    return orbs

