
def _assert_rank_and_shape_compatibility(tensors, rank):
  if not tensors:
    raise ValueError("List of tensors cannot be empty")

  tmp_shape = tensors[0].shape
  for tensor in tensors:
    if tensor.ndim != rank:
      raise ValueError("Shape %s must have rank %d" % (tensor.ndim, rank))
    if tensor.shape != tmp_shape:
      raise ValueError("Shapes %s and %s are not compatible" %
                       (tensor.shape, tmp_shape))

