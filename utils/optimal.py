import itertools
from typing import Dict, List, Optional, Tuple

def optimal(
    inputs: List[ArrayIndexType],
    output: ArrayIndexType,
    size_dict: Dict[str, int],
    memory_limit: Optional[int] = None,
) -> PathType:
    """Computes all possible pair contractions in a depth-first recursive manner,
    sieving results based on `memory_limit` and the best path found so far.

    Parameters:
        inputs: List of sets that represent the lhs side of the einsum subscript.
        output: Set that represents the rhs side of the overall einsum subscript.
        size_dict: Dictionary of index sizes.
        memory_limit: The maximum number of elements in a temporary array.

    Returns:
        path: The optimal contraction order within the memory limit constraint.

    Examples:
    ```python
    isets = [set('abd'), set('ac'), set('bdc')]
    oset = set('')
    idx_sizes = {'a': 1, 'b':2, 'c':3, 'd':4}
    optimal(isets, oset, idx_sizes, 5000)
    #> [(0, 2), (0, 1)]
    ```
    """
    inputs_set = tuple(map(frozenset, inputs))
    output_set = frozenset(output)

    best_flops = {"flops": float("inf")}
    best_ssa_path = {"ssa_path": (tuple(range(len(inputs))),)}
    size_cache: Dict[FrozenSet[str], int] = {}
    result_cache: Dict[Tuple[ArrayIndexType, ArrayIndexType], Tuple[FrozenSet[str], int]] = {}

    def _optimal_iterate(path, remaining, inputs, flops):
        # reached end of path (only ever get here if flops is best found so far)
        if len(remaining) == 1:
            best_flops["flops"] = flops
            best_ssa_path["ssa_path"] = path
            return

        # check all possible remaining paths
        for i, j in itertools.combinations(remaining, 2):
            if i > j:
                i, j = j, i
            key = (inputs[i], inputs[j])
            try:
                k12, flops12 = result_cache[key]
            except KeyError:
                k12, flops12 = result_cache[key] = calc_k12_flops(inputs, output_set, remaining, i, j, size_dict)

            # sieve based on current best flops
            new_flops = flops + flops12
            if new_flops >= best_flops["flops"]:
                continue

            # sieve based on memory limit
            if memory_limit not in _UNLIMITED_MEM:
                try:
                    size12 = size_cache[k12]
                except KeyError:
                    size12 = size_cache[k12] = compute_size_by_dict(k12, size_dict)

                # possibly terminate this path with an all-terms einsum
                if size12 > memory_limit:
                    new_flops = flops + _compute_oversize_flops(inputs, remaining, output_set, size_dict)
                    if new_flops < best_flops["flops"]:
                        best_flops["flops"] = new_flops
                        best_ssa_path["ssa_path"] = path + (tuple(remaining),)
                    continue

            # add contraction and recurse into all remaining
            _optimal_iterate(
                path=path + ((i, j),),
                inputs=inputs + (k12,),
                remaining=remaining - {i, j} | {len(inputs)},
                flops=new_flops,
            )

    _optimal_iterate(path=(), inputs=inputs_set, remaining=set(range(len(inputs))), flops=0)

    return ssa_to_linear(best_ssa_path["ssa_path"])

