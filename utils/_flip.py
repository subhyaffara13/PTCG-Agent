
def _flip(m: Array, axis: int | tuple[int, ...] | None = None) -> Array:
  if axis is None:
    return lax.rev(m, list(range(len(np.shape(m)))))
  axis = _ensure_index_tuple(axis)
  return lax.rev(m, [_canonicalize_axis(ax, np.ndim(m)) for ax in axis])

