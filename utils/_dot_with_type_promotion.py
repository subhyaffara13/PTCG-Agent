
def _dot_with_type_promotion(u, v):
    if u.dim() != 1 or v.dim() != 1:
        raise AssertionError(
            f"Expected u and v to be 1D tensors, but got dims {u.dim()} and {v.dim()}"
        )
    return (u * v).sum()

