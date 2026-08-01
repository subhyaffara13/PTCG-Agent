
def _naive_list_centralizer(self, other, af=False):
    from sympy.combinatorics.perm_groups import PermutationGroup
    """
    Return a list of elements for the centralizer of a subgroup/set/element.

    Explanation
    ===========

    This is a brute force implementation that goes over all elements of the
    group and checks for membership in the centralizer. It is used to
    test ``.centralizer()`` from ``sympy.combinatorics.perm_groups``.

    Examples
    ========

    >>> from sympy.combinatorics.testutil import _naive_list_centralizer
    >>> from sympy.combinatorics.named_groups import DihedralGroup
    >>> D = DihedralGroup(4)
    >>> _naive_list_centralizer(D, D)
    [Permutation([0, 1, 2, 3]), Permutation([2, 3, 0, 1])]

    See Also
    ========

    sympy.combinatorics.perm_groups.centralizer

    """
    from sympy.combinatorics.permutations import _af_commutes_with
    if hasattr(other, 'generators'):
        elements = list(self.generate_dimino(af=True))
        gens = [x._array_form for x in other.generators]
        commutes_with_gens = lambda x: all(_af_commutes_with(x, gen) for gen in gens)
        centralizer_list = []
        if not af:
            for element in elements:
                if commutes_with_gens(element):
                    centralizer_list.append(Permutation._af_new(element))
        else:
            for element in elements:
                if commutes_with_gens(element):
                    centralizer_list.append(element)
        return centralizer_list
    elif hasattr(other, 'getitem'):
        return _naive_list_centralizer(self, PermutationGroup(other), af)
    elif hasattr(other, 'array_form'):
        return _naive_list_centralizer(self, PermutationGroup([other]), af)

