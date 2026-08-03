from typing import Any, Dict, List, Optional, Set, Tuple, Union

def _dp_compare_flops(
    cost1: int,
    cost2: int,
    i1_union_i2: Set[int],
    size_dict: List[int],
    cost_cap: int,
    s1: int,
    s2: int,
    xn: Dict[int, Any],
    g: int,
    all_tensors: int,
    inputs: List[FrozenSet[int]],
    i1_cut_i2_wo_output: Set[int],
    memory_limit: Optional[int],
    contract1: Union[int, Tuple[int]],
    contract2: Union[int, Tuple[int]],
) -> None:
    """Performs the inner comparison of whether the two subgraphs (the bitmaps
    `s1` and `s2`) should be merged and added to the dynamic programming
    search. Will skip for a number of reasons:

    1. If the number of operations to form `s = s1 | s2` including previous
       contractions is above the cost-cap.
    2. If we've already found a better way of making `s`.
    3. If the intermediate tensor corresponding to `s` is going to break the
       memory limit.
    """
    # TODO: Odd usage with an Iterable[int] to map a dict of type List[int]
    cost = cost1 + cost2 + compute_size_by_dict(i1_union_i2, size_dict)
    if cost <= cost_cap:
        s = s1 | s2
        if s not in xn or cost < xn[s][1]:
            i = _dp_calc_legs(g, all_tensors, s, inputs, i1_cut_i2_wo_output, i1_union_i2)
            mem = compute_size_by_dict(i, size_dict)
            if memory_limit is None or mem <= memory_limit:
                xn[s] = (i, cost, (contract1, contract2))

