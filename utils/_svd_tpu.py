import functools

def _svd_tpu(a, *, full_matrices, compute_uv, subset_by_index, algorithm=None):
  if algorithm is not None and algorithm != lax_linalg.SvdAlgorithm.DEFAULT:
    raise NotImplementedError(
        "The SVD algorithm parameter is not implemented on TPU.")

  batch_dims = a.shape[:-2]
  fn = functools.partial(
      svd,
      full_matrices=full_matrices,
      compute_uv=compute_uv,
      subset_by_index=subset_by_index,
  )
  for _ in range(len(batch_dims)):
    fn = api.vmap(fn)

  if compute_uv:
    u, s, vh = fn(a)
    return [s, u, vh]
  else:
    s = fn(a)
    return [s]

