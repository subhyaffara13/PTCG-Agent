
def _is_nonempty(x: ArrayLike, axis: AxisInt) -> bool:
    # filter empty arrays
    # 1-d dtypes always are included here
    if x.ndim <= axis:
        return True
    return x.shape[axis] > 0

