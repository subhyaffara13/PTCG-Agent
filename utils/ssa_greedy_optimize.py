import itertools
from typing import Any, Dict, List

def ssa_greedy_optimize(
    inputs: List[ArrayIndexType],
    output: ArrayIndexType,
    sizes: Dict[str, int],
    choose_fn: Any = None,
    cost_fn: Any = "memory-removed",
) -> PathType:
    """This is the core function for :func:`greedy` but produces a path with
    static single assignment ids rather than recycled linear ids.
    SSA ids are cheaper to work with and easier to reason about.
    """
    if len(inputs) == 1:
        # Perform a single contraction to match output shape.
        return [(0,)]

    # set the function that assigns a heuristic cost to a possible contraction
    cost_fn = _COST_FNS.get(cost_fn, cost_fn)

    # set the function that chooses which contraction to take
    if choose_fn is None:
        choose_fn = _simple_chooser
        push_all = False
    else:
        # assume chooser wants access to all possible contractions
        push_all = True

    # A dim that is common to all tensors might as well be an output dim, since it
    # cannot be contracted until the final step. This avoids an expensive all-pairs
    # comparison to search for possible contractions at each step, leading to speedup
    # in many practical problems where all tensors share a common batch dimension.
    fs_inputs = [frozenset(x) for x in inputs]
    output = frozenset(output) | frozenset.intersection(*fs_inputs)

    # Deduplicate shapes by eagerly computing Hadamard products.
    remaining: Dict[ArrayIndexType, int] = {}  # key -> ssa_id
    ssa_ids = itertools.count(len(fs_inputs))
    ssa_path: List[TensorShapeType] = []
    for ssa_id, key in enumerate(fs_inputs):
        if key in remaining:
            ssa_path.append((remaining[key], ssa_id))
            remaining[key] = next(ssa_ids)
        else:
            remaining[key] = ssa_id

    # Keep track of possible contraction dims.
    dim_to_keys = defaultdict(set)
    for key in remaining:
        for dim in key - output:
            dim_to_keys[dim].add(key)

    # Keep track of the number of tensors using each dim; when the dim is no longer
    # used it can be contracted. Since we specialize to binary ops, we only care about
    # ref counts of >=2 or >=3.
    dim_ref_counts = {
        count: {dim for dim, keys in dim_to_keys.items() if len(keys) >= count} - output for count in [2, 3]
    }

    # Compute separable part of the objective function for contractions.
    footprints = {key: compute_size_by_dict(key, sizes) for key in remaining}

    # Find initial candidate contractions.
    queue: List[GreedyContractionType] = []
    for dim, dim_keys in dim_to_keys.items():
        dim_keys_list = sorted(dim_keys, key=remaining.__getitem__)
        for i, k1 in enumerate(dim_keys_list[:-1]):
            k2s_guess = dim_keys_list[1 + i :]
            _push_candidate(
                output,
                sizes,
                remaining,
                footprints,
                dim_ref_counts,
                k1,
                k2s_guess,
                queue,
                push_all,
                cost_fn,
            )

    # Greedily contract pairs of tensors.
    while queue:
        con = choose_fn(queue, remaining)
        if con is None:
            continue  # allow choose_fn to flag all candidates obsolete
        cost, k1, k2, k12 = con

        ssa_id1 = remaining.pop(k1)
        ssa_id2 = remaining.pop(k2)
        for dim in k1 - output:
            dim_to_keys[dim].remove(k1)
        for dim in k2 - output:
            dim_to_keys[dim].remove(k2)
        ssa_path.append((ssa_id1, ssa_id2))
        if k12 in remaining:
            ssa_path.append((remaining[k12], next(ssa_ids)))
        else:
            for dim in k12 - output:
                dim_to_keys[dim].add(k12)
        remaining[k12] = next(ssa_ids)
        _update_ref_counts(dim_to_keys, dim_ref_counts, k1 | k2 - output)
        footprints[k12] = compute_size_by_dict(k12, sizes)

        # Find new candidate contractions.
        k1 = k12
        k2s = {k2 for dim in k1 for k2 in dim_to_keys[dim]}
        k2s.discard(k1)
        if k2s:
            _push_candidate(
                output,
                sizes,
                remaining,
                footprints,
                dim_ref_counts,
                k1,
                list(k2s),
                queue,
                push_all,
                cost_fn,
            )

    # Greedily compute pairwise outer products.
    final_queue = [(compute_size_by_dict(key & output, sizes), ssa_id, key) for key, ssa_id in remaining.items()]
    heapq.heapify(final_queue)
    _, ssa_id1, k1 = heapq.heappop(final_queue)
    while final_queue:
        _, ssa_id2, k2 = heapq.heappop(final_queue)
        ssa_path.append((min(ssa_id1, ssa_id2), max(ssa_id1, ssa_id2)))
        k12 = (k1 | k2) & output
        cost = compute_size_by_dict(k12, sizes)
        ssa_id12 = next(ssa_ids)
        _, ssa_id1, k1 = heapq.heappushpop(final_queue, (cost, ssa_id12, k12))

    return ssa_path

