
def get_placement_from_reduction_op(reduction_op: ReductionOpType) -> Placement:
    if isinstance(reduction_op, NormReduction):
        if reduction_op.norm_type == 0:
            # return P(sum) for easier reduction_linear handling.
            return Partial("sum")
        return _NormPartial(norm_type=reduction_op.norm_type)
    return Partial(reduction_op)

