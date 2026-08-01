
def to_numpy_type(number_type):
  if np is not None:
    return np.dtype(number_type.name).newbyteorder("<")
  else:
    raise NumpyRequiredForThisFeature("Numpy was not found.")

