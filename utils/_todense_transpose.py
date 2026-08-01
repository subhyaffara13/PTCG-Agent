
def _todense_transpose(ct, *bufs, tree):
  assert ad.is_undefined_primal(bufs[0])
  assert not any(ad.is_undefined_primal(buf) for buf in bufs[1:])

  standin = object()
  obj = tree_util.tree_unflatten(tree, [standin] * len(bufs))
  from jax.experimental.sparse import BCOO, BCSR
  from jax.experimental.sparse.bcoo import _bcoo_extract
  from jax.experimental.sparse.bcsr import bcsr_extract
  if obj is standin:
    return (ct,)
  elif isinstance(obj, BCOO):
    _, indices = bufs
    return _bcoo_extract(indices, ct), indices
  elif isinstance(obj, BCSR):
    _, indices, indptr = bufs
    return bcsr_extract(indices, indptr, ct), indices, indptr
  elif isinstance(obj, COO):
    _, row, col = bufs
    return _coo_extract(row, col, ct), row, col
  else:
    raise NotImplementedError(f"todense_transpose for {type(obj)}")

