
def pretty_nd_slice(idx: Sequence[slice] | type(Ellipsis)) -> str:
  """Returns a pretty-printed string representation of a NdSlice."""
  idx_str = (
      '...'
      if not idx or idx is Ellipsis
      else ', '.join(_pretty_slice(s) for s in idx)
  )
  return f'np.s_[{idx_str}]'

