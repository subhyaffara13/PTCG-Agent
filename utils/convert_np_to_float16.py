
def convert_np_to_float16(np_array, min_positive_val=5.96e-08, max_finite_val=65504.0):
    """
    Convert float32 numpy array to float16 without changing sign or finiteness.
    Positive values less than min_positive_val are mapped to min_positive_val.
    Positive finite values greater than max_finite_val are mapped to max_finite_val.
    Similar for negative values. NaN, 0, inf, and -inf are unchanged.
    """

    def between(a, b, c):
        return np.logical_and(a < b, b < c)

    if np_array[np.where(np_array > 0)].shape[0] > 0:
        positive_max = np_array[np.where(np_array > 0)].max()
        positive_min = np_array[np.where(np_array > 0)].min()
        if positive_max >= max_finite_val:
            logger.debug(f"the float32 number {positive_max} will be truncated to {max_finite_val}")
        if positive_min <= min_positive_val:
            logger.debug(f"the float32 number {positive_min} will be truncated to {min_positive_val}")

    if np_array[np.where(np_array < 0)].shape[0] > 0:
        negative_max = np_array[np.where(np_array < 0)].max()
        negative_min = np_array[np.where(np_array < 0)].min()
        if negative_min <= -max_finite_val:
            logger.debug(f"the float32 number {negative_min} will be truncated to {-max_finite_val}")
        if negative_max >= -min_positive_val:
            logger.debug(f"the float32 number {negative_max} will be truncated to {-min_positive_val}")

    np_array = np.where(between(0, np_array, min_positive_val), min_positive_val, np_array)
    np_array = np.where(between(-min_positive_val, np_array, 0), -min_positive_val, np_array)
    np_array = np.where(between(max_finite_val, np_array, float("inf")), max_finite_val, np_array)
    np_array = np.where(between(float("-inf"), np_array, -max_finite_val), -max_finite_val, np_array)
    return np.float16(np_array)

