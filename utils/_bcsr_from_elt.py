
def _bcsr_from_elt(cont, axis_size, elt, axis):
  if axis is None:
    return elt
  if axis > elt.n_batch:
    raise ValueError(f"BCSR: cannot add out_axis={axis} for BCSR array with "
                     f"n_batch={elt.n_batch}. BCSR batch axes must be a "
                     "contiguous block of leading dimensions.")
  return BCSR((cont(axis_size, elt.data, axis),
               cont(axis_size, elt.indices, axis),
               cont(axis_size, elt.indptr, axis)),
              shape=elt.shape[:axis] + (axis_size,) + elt.shape[axis:])

