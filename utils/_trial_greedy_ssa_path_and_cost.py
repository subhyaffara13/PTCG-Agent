from typing import Any, Dict, List, Tuple

def _trial_greedy_ssa_path_and_cost(
    r: int,
    inputs: List[ArrayIndexType],
    output: ArrayIndexType,
    size_dict: Dict[str, int],
    choose_fn: Any,
    cost_fn: Any,
) -> Tuple[PathType, int, int]:
    """A single, repeatable, greedy trial run. **Returns:** ``ssa_path`` and cost."""
    if r == 0:
        # always start with the standard greedy approach
        choose_fn = None

    random_seed(r)

    ssa_path = paths.ssa_greedy_optimize(inputs, output, size_dict, choose_fn, cost_fn)
    cost, size = ssa_path_compute_cost(ssa_path, inputs, output, size_dict)

    return ssa_path, cost, size

