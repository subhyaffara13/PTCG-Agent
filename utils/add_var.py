
def add_var(
    val: float,
    nobs: int,
    mean_x: float,
    ssqdm_x: float,
    compensation: float,
    num_consecutive_same_value: int,
    prev_value: float,
) -> tuple[int, float, float, float, int, float]:
    if not np.isnan(val):
        if val == prev_value:
            num_consecutive_same_value += 1
        else:
            num_consecutive_same_value = 1
        prev_value = val

        nobs += 1
        prev_mean = mean_x - compensation
        y = val - compensation
        t = y - mean_x
        compensation = t + mean_x - y
        delta = t
        if nobs:
            mean_x += delta / nobs
        else:
            mean_x = 0
        ssqdm_x += (val - prev_mean) * (val - mean_x)
    return nobs, mean_x, ssqdm_x, compensation, num_consecutive_same_value, prev_value

