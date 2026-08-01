
def _orbit(degree, generators, alpha, action='tuples'):
    r"""Compute the orbit of alpha `\{g(\alpha) | g \in G\}` as a set.

    Explanation
    ===========

    The time complexity of the algorithm used here is `O(|Orb|*r)` where
    `|Orb|` is the size of the orbit and ``r`` is the number of generators of
    the group. For a more detailed analysis, see [1], p.78, [2], pp. 19-21.
    Here alpha can be a single point, or a list of points.

    If alpha is a single point, the ordinary orbit is computed.
    if alpha is a list of points, there are three available options:

    'union' - computes the union of the orbits of the points in the list
    'tuples' - computes the orbit of the list interpreted as an ordered
    tuple under the group action ( i.e., g((1, 2, 3)) = (g(1), g(2), g(3)) )
    'sets' - computes the orbit of the list interpreted as a sets

    Examples
    ========

    >>> from sympy.combinatorics import Permutation, PermutationGroup
    >>> from sympy.combinatorics.perm_groups import _orbit
    >>> a = Permutation([1, 2, 0, 4, 5, 6, 3])
    >>> G = PermutationGroup([a])
    >>> _orbit(G.degree, G.generators, 0)
    {0, 1, 2}
    >>> _orbit(G.degree, G.generators, [0, 4], 'union')
    {0, 1, 2, 3, 4, 5, 6}

    See Also
    ========

    orbit, orbit_transversal

    """
    if not hasattr(alpha, '__getitem__'):
        alpha = [alpha]

    gens = [x._array_form for x in generators]
    if len(alpha) == 1 or action == 'union':
        orb = alpha
        used = [False]*degree
        for el in alpha:
            used[el] = True
        for b in orb:
            for gen in gens:
                temp = gen[b]
                if used[temp] == False:
                    orb.append(temp)
                    used[temp] = True
        return set(orb)
    elif action == 'tuples':
        alpha = tuple(alpha)
        orb = [alpha]
        used = {alpha}
        for b in orb:
            for gen in gens:
                temp = tuple([gen[x] for x in b])
                if temp not in used:
                    orb.append(temp)
                    used.add(temp)
        return set(orb)
    elif action == 'sets':
        alpha = frozenset(alpha)
        orb = [alpha]
        used = {alpha}
        for b in orb:
            for gen in gens:
                temp = frozenset([gen[x] for x in b])
                if temp not in used:
                    orb.append(temp)
                    used.add(temp)
        return {tuple(x) for x in orb}

