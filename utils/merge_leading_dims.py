
def merge_leading_dims(x, num_dims):
  """Merge leading dimensions."""
  # Don't merge if there aren't dimensions to merge.
  if not ndim_at_least(x, num_dims):
    return x

  new_shape = (np.prod(x.shape[:num_dims]),) + x.shape[num_dims:]
  return x.reshape(new_shape)

