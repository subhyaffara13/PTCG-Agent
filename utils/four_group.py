
def four_group():
    """
    Return a representation of the Klein four-group as a transitive subgroup
    of S4.
    """
    return PermutationGroup(
        Permutation(0, 1)(2, 3),
        Permutation(0, 2)(1, 3)
    )

