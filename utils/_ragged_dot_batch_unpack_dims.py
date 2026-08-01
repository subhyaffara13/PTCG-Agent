
def _ragged_dot_batch_unpack_dims(batch_dims):
  if not all(dim == 0 for dim in batch_dims):
    raise NotImplementedError('ragged_dot vmap over any dim but 0 - NYI')
  lbd, rbd, _ = batch_dims
  return (lbd, rbd)

