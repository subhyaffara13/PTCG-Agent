from typing import Dict, List, Tuple

def ssa_path_compute_cost(
    ssa_path: PathType,
    inputs: List[ArrayIndexType],
    output: ArrayIndexType,
    size_dict: Dict[str, int],
) -> Tuple[int, int]:
    """Compute the flops and max size of an ssa path."""
    inputs = list(map(frozenset, inputs))
    output = frozenset(output)
    remaining = set(range(len(inputs)))
    total_cost = 0
    max_size = 0

    for i, j in ssa_path:
        k12, flops12 = paths.calc_k12_flops(inputs, output, remaining, i, j, size_dict)  # type: ignore
        remaining.discard(i)
        remaining.discard(j)
        remaining.add(len(inputs))
        inputs.append(k12)
        total_cost += flops12
        max_size = max(max_size, helpers.compute_size_by_dict(k12, size_dict))

    return total_cost, max_size

