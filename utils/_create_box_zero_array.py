
def _create_box_zero_array(space: Box):
    zero_array = np.zeros(space.shape, dtype=space.dtype)
    zero_array = np.where(space.low > 0, space.low, zero_array)
    zero_array = np.where(space.high < 0, space.high, zero_array)
    return zero_array

