
def _make_array_cls_name(np_dtype: np.dtype) -> str:
  """Makes the array class name for the dtype."""
  kind_str = _NP_KIND_TO_STR[np_dtype.kind]
  if np_dtype.kind in _BITS_KINDS:
    # Display with the size (ui8, f32,...)
    return f'{kind_str}{np_dtype.itemsize * 8}'
  else:
    return kind_str  # Raw types (str, bool_,...)

