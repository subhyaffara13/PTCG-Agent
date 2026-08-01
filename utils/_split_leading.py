
def _split_leading(sz, x):
  return (slicing.slice_in_dim(x, 0, sz),
          slicing.slice_in_dim(x, sz, x.shape[0]))

