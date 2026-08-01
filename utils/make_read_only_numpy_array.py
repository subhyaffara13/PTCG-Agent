
def make_read_only_numpy_array():
  values = np.zeros(5, dtype=np.int32)
  values.flags.writeable = False
  return values

