
def _bcsr_to_elt(cont, _, val, axis):
  if axis is None:
    return val
  if axis >= val.n_batch:
    raise ValueError(f"Cannot map in_axis={axis} for BCSR array with n_batch="
                     f"{val.n_batch}. in_axes for batched BCSR operations must "
                     "correspond to a batched dimension.")
  return BCSR((cont(val.data, axis),
               cont(val.indices, axis),
               cont(val.indptr, axis)),
              shape=val.shape[:axis] + val.shape[axis + 1:])

