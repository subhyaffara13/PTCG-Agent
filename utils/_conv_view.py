
def _conv_view(lhs, rhs_shape, window_strides, pads, pad_value):
  """Compute the view (and its axes) of a convolution or window reduction."""
  if (_min(lhs.ndim, len(rhs_shape)) < 2 or lhs.ndim != len(rhs_shape)
      or lhs.shape[1] != rhs_shape[1]):
    raise ValueError('Dimension mismatch')
  if len(window_strides) != len(rhs_shape) - 2:
    raise ValueError('Wrong number of strides for spatial dimensions')
  if len(pads) != len(rhs_shape) - 2:
    raise ValueError('Wrong number of pads for spatial dimensions')

  lhs = _pad(lhs, [(0, 0)] * 2 + list(pads), pad_value)
  in_shape = lhs.shape[2:]
  filter_shape = rhs_shape[2:]
  dim = len(filter_shape)  # number of 'spatial' dimensions in convolution

  out_strides = np.multiply(window_strides, lhs.strides[2:])
  view_strides = lhs.strides[:1] + tuple(out_strides) + lhs.strides[1:]

  out_shape = np.floor_divide(
      np.subtract(in_shape, filter_shape), window_strides) + 1
  view_shape = lhs.shape[:1] + tuple(out_shape) + rhs_shape[1:]

  view = np.lib.stride_tricks.as_strided(lhs, view_shape, view_strides)

  view_axes = list(range(view.ndim))
  sum_axes = view_axes[-dim-1:]
  rhs_axes = [view.ndim] + sum_axes
  out_axes = [0, view.ndim] + list(range(1, dim+1))

  return view, view_axes, rhs_axes, out_axes

