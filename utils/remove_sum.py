from typing import Any

def remove_sum(
    val: Any, nobs: int, sum_x: Any, compensation: Any
) -> tuple[int, Any, Any]:
    if not np.isnan(val):
        nobs -= 1
        y = -val - compensation
        t = sum_x + y
        compensation = t - sum_x - y
        sum_x = t
    return nobs, sum_x, compensation

