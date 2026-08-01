
def philox_fold_in(key, data):
  assert data.ndim == 0
  return philox_4x32_count(key, (), offset=data, fuse_output=False)

