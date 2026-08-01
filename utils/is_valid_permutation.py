
def is_valid_permutation(rank: int, perm: DimsSequenceType) -> bool:
    """
    Validates that perm is a permutation of length rank.
    """

    return isinstance(perm, Sequence) and sorted(perm) == list(range(rank))

