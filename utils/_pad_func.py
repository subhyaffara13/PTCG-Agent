
def _pad_func(array: Array, pad_width: PadValue[int], func: Callable[..., Any], **kwargs) -> Array:
  pad_width = _broadcast_to_pairs(pad_width, np.ndim(array), "pad_width")
  padded = _pad_constant(array, pad_width, asarray(0))
  for axis in range(np.ndim(padded)):
    padded = apply_along_axis(func, axis, padded, pad_width[axis], axis, kwargs)
  return padded

