
def get_numeric_mat(shape):
    arr = np.arange(shape[0])
    return np.lib.stride_tricks.as_strided(
        x=arr, shape=shape, strides=(arr.itemsize,) + (0,) * (len(shape) - 1)
    ).copy()

