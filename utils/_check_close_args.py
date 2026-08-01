
def _check_close_args(
    name: str,
    a: TensorLikeType,
    b: TensorLikeType,
    rtol: float,
    atol: float,
) -> None:
    torch._check_value(
        a.dtype == b.dtype,
        lambda: f"{name}: Attempting to compare tensors of different dtypes {a.dtype} and {b.dtype}!",
    )
    torch._check(
        rtol >= 0,
        lambda: f"{name}: rtol must be greater than or equal to zero, but got {rtol}!",
    )
    torch._check(
        atol >= 0,
        lambda: f"{name}: atol must be greater than or equal to zero, but got {atol}!",
    )

