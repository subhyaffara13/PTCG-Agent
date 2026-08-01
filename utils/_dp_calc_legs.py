
def _dp_calc_legs(g, all_tensors, s, inputs, i1_cut_i2_wo_output, i1_union_i2):
    """Calculates the effective outer indices of the intermediate tensor
    corresponding to the subgraph ``s``.
    """
    # set of remaining tensors (=g-s)
    r = g & (all_tensors ^ s)
    # indices of remaining indices:
    if r:
        i_r = frozenset.union(*_bitmap_select(r, inputs))
    else:
        i_r = frozenset()
    # contraction indices:
    i_contract = i1_cut_i2_wo_output - i_r
    return i1_union_i2 - i_contract

