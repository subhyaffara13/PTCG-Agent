
def _dp_compare_size(
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
    """Like `_dp_compare_flops` but sieves the potential contraction based
    on the size of the intermediate tensor created, rather than the number of
    operations, and so calculates that first.
    """
    s = s1 | s2
    i = _dp_calc_legs(g, all_tensors, s, inputs, i1_cut_i2_wo_output, i1_union_i2)
    mem = compute_size_by_dict(i, size_dict)
    cost = max(cost1, cost2, mem)
    if cost <= cost_cap:
        if s not in xn or cost < xn[s][1]:
            if memory_limit is None or mem <= memory_limit:
                xn[s] = (i, cost, (contract1, contract2))

