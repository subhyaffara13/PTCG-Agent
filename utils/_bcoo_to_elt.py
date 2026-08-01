
def _bcoo_to_elt(cont, _, val, axis):
  if axis is None:
    return val
  if axis >= val.n_batch:
    raise ValueError(f"Cannot map in_axis={axis} for BCOO array with n_batch={val.n_batch}. "
                     "in_axes for batched BCOO operations must correspond to a batch dimension.")
  return BCOO((cont(val.data, axis), cont(val.indices, axis)),
              shape=val.shape[:axis] + val.shape[axis + 1:],
              indices_sorted=val.indices_sorted, unique_indices=val.unique_indices)

