
def _reduction_int_to_str(reduction: int) -> str:
    from torch._decomp.decompositions import Reduction

    if reduction == Reduction.NONE.value:
        return "none"
    elif reduction == Reduction.MEAN.value:
        return "mean"
    elif reduction == Reduction.SUM.value:
        return "sum"
    else:
        raise ValueError(f"{reduction} is not a valid value for reduction")

