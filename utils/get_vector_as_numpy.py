
def GetVectorAsNumpy(numpy_type, buf, count, offset):
  """GetVecAsNumpy decodes values starting at buf[head] as

  `numpy_type`, where `numpy_type` is a numpy dtype.
  """
  if np is not None:
    # TODO: could set .flags.writeable = False to make users jump through
    #       hoops before modifying...
    return np.frombuffer(buf, dtype=numpy_type, count=count, offset=offset)
  else:
    raise NumpyRequiredForThisFeature('Numpy was not found.')

