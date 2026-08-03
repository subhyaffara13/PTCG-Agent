from typing import Any

def add_sum(
    val: Any,
    nobs: int,
    sum_x: Any,
    compensation: Any,
    num_consecutive_same_value: int,
    prev_value: Any,
) -> tuple[int, Any, Any, int, Any]:
    if not np.isnan(val):
        nobs += 1
        y = val - compensation
        t = sum_x + y
        compensation = t - sum_x - y
        sum_x = t

        if val == prev_value:
            num_consecutive_same_value += 1
        else:
            num_consecutive_same_value = 1
        prev_value = val

    return nobs, sum_x, compensation, num_consecutive_same_value, prev_value

