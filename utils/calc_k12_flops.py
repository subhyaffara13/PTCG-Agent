
def calc_k12_flops(
    inputs: Tuple[FrozenSet[str]],
    output: FrozenSet[str],
    remaining: FrozenSet[int],
    i: int,
    j: int,
    size_dict: Dict[str, int],
) -> Tuple[FrozenSet[str], int]:
    """Calculate the resulting indices and flops for a potential pairwise
    contraction - used in the recursive (optimal/branch) algorithms.

    Parameters:
        inputs: The indices of each tensor in this contraction, note this includes
            tensors unavailable to contract as static single assignment is used:>
            contracted tensors are not removed from the list.
        output: The set of output indices for the whole contraction.
        remaining: *The set of indices (corresponding to ``inputs``) of tensors still available to contract.
        i: Index of potential tensor to contract.
        j: Index of potential tensor to contract.
        size_dict: Size mapping of all the indices.

    Returns:
        k12: The resulting indices of the potential tensor.
        cost: Estimated flop count of operation.
    """
    k1, k2 = inputs[i], inputs[j]
    either = k1 | k2
    shared = k1 & k2
    keep = frozenset.union(output, *map(inputs.__getitem__, remaining - {i, j}))

    k12 = either & keep
    cost = flop_count(either, bool(shared - keep), 2, size_dict)

    return k12, cost

