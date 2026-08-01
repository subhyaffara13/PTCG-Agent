
def assert_is_1d_numpy_array(array):
  if not isinstance(array, np.ndarray):
    raise ValueError("The argument must be a numpy array, not a {}.".format(
        type(array)))

  if len(array.shape) != 1:
    raise ValueError(
        "The argument must be 1-dimensional, not of shape {}.".format(
            array.shape))

