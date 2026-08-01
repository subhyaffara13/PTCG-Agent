
def _verify_normal_closure(group, arg, closure=None):
    from sympy.combinatorics.perm_groups import PermutationGroup
    """
    Verify the normal closure of a subgroup/subset/element in a group.

    This is used to test
    sympy.combinatorics.perm_groups.PermutationGroup.normal_closure

    Examples
    ========

    >>> from sympy.combinatorics.named_groups import (SymmetricGroup,
    ... AlternatingGroup)
    >>> from sympy.combinatorics.testutil import _verify_normal_closure
    >>> S = SymmetricGroup(3)
    >>> A = AlternatingGroup(3)
    >>> _verify_normal_closure(S, A, closure=A)
    True

    See Also
    ========

    sympy.combinatorics.perm_groups.PermutationGroup.normal_closure

    """
    if closure is None:
        closure = group.normal_closure(arg)
    conjugates = set()
    if hasattr(arg, 'generators'):
        subgr_gens = arg.generators
    elif hasattr(arg, '__getitem__'):
        subgr_gens = arg
    elif hasattr(arg, 'array_form'):
        subgr_gens = [arg]
    for el in group.generate_dimino():
        conjugates.update(gen ^ el for gen in subgr_gens)
    naive_closure = PermutationGroup(list(conjugates))
    return closure.is_subgroup(naive_closure)

