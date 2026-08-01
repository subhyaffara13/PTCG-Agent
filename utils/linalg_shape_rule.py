
def linalg_shape_rule(multiple_results, supports_batching, ranks, result_shape,
                      name, *avals, **kwargs):
  batch_dims, dims = [], []
  for i, (rank, aval) in enumerate(zip(ranks, avals)):
    shape = aval.shape
    if len(shape) < rank:
      raise TypeError(
          f"Input {i} to {name} must have rank at least {rank}, but got "
          f"shape={shape}"
      )
    if not supports_batching and len(shape) != rank:
      raise TypeError(
          f"Input {i} to {name} must have a rank of exactly {rank}, but got "
          f"shape={shape}"
      )
    batch_dims.append(shape[:len(shape) - rank])
    dims.append(shape[len(shape) - rank:])
  if not all(len(batch_dims[0]) == len(b) for b in batch_dims):
    raise TypeError(
        f"All inputs to {name} must have the same number of batch dimensions, "
        f"but got {[len(b) for b in batch_dims]} batch dimensions for the "
        "inputs."
    )
  batch_dims = tuple(batch_dims[0])
  out = result_shape(*dims, **kwargs)
  if multiple_results:
    return tuple(batch_dims + tuple(d) for d in out)
  else:
    return batch_dims + tuple(out)

