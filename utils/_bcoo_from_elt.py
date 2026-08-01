
def _bcoo_from_elt(cont, axis_size, elt, axis):
  if axis is None:
    return elt
  if axis > elt.n_batch:
    raise ValueError(f"BCOO: cannot add out_axis={axis} for BCOO array with n_batch={elt.n_batch}. "
                     "BCOO batch axes must be a contiguous block of leading dimensions.")
  return BCOO((cont(axis_size, elt.data, axis), cont(axis_size, elt.indices, axis)),
              shape=elt.shape[:axis] + (axis_size,) + elt.shape[axis:],
              indices_sorted=elt.indices_sorted, unique_indices=elt.unique_indices)

