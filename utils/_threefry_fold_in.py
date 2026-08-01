
def _threefry_fold_in(key, data):
  return threefry_2x32(key, threefry_seed(data))

