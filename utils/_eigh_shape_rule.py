
def _eigh_shape_rule(shape, *, subset_by_index, **_):
  if shape[0] != shape[-1]:
    raise ValueError(
        "Argument to symmetric eigendecomposition must have shape [..., n, n], "
        f"got shape {shape}"
    )
  n = shape[0]
  d = (n if subset_by_index is None else
       subset_by_index[1] - subset_by_index[0])
  return (n, d), (d,)

