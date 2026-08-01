
def maybe_wrap_dim(dim: int, dim_post_expr: int, wrap_scalar: bool = True):
    if dim_post_expr <= 0:
        if not wrap_scalar:
            raise AssertionError(
                f"dim_post_expr={dim_post_expr} <= 0 but wrap_scalar is False"
            )
        dim_post_expr = 1
    min = -dim_post_expr
    max = dim_post_expr - 1
    if dim < min or dim > max:
        raise AssertionError(f"dim {dim} out of bounds ({min}, {max})")
    if dim < 0:
        dim += dim_post_expr
    return dim


def maybe_wrap_dim(dim: int, dim_post_expr: int, wrap_scalar: bool = True):
    if dim_post_expr <= 0:
        if not wrap_scalar:
            raise AssertionError(
                "Expected wrap_scalar to be True when dim_post_expr <= 0"
            )
        dim_post_expr = 1
    min = -dim_post_expr
    max = dim_post_expr - 1
    if dim < min or dim > max:
        raise AssertionError(
            f"Dimension {dim} out of range (expected to be in range [{min}, {max}])"
        )
    if dim < 0:
        dim += dim_post_expr
    return dim

