
def _conv(obj, dtype=None):
    """ Convert an object to the preferred form for input to the odr routine.
    """

    if obj is None:
        return obj
    else:
        if dtype is None:
            obj = np.asarray(obj)
        else:
            obj = np.asarray(obj, dtype)
        if obj.shape == ():
            # Scalar.
            return obj.dtype.type(obj)
        else:
            return obj


def _conv(lhs, rhs, window_strides, pads):
  view, view_axes, rhs_axes, out_axes = _conv_view(
      lhs, rhs.shape, window_strides, pads, 0.)
  return opt_einsum.contract(
      view, view_axes, rhs, rhs_axes, out_axes, use_blas=True)


def _conv(x: Array, y: Array, mode: str, op: str, precision: lax.PrecisionLike,
          preferred_element_type: DTypeLike | None = None) -> Array:
  if np.ndim(x) != 1 or np.ndim(y) != 1:
    raise ValueError(f"{op}() only support 1-dimensional inputs.")
  if preferred_element_type is None:
    # if unspecified, promote to inexact following NumPy's default for convolutions.
    x, y = util.promote_dtypes_inexact(x, y)
  else:
    # otherwise cast to same type but otherwise preserve input dtypes
    x, y = util.promote_dtypes(x, y)
  if len(x) == 0 or len(y) == 0:
    raise ValueError(f"{op}: inputs cannot be empty, got shapes {x.shape} and {y.shape}.")

  out_order = slice(None)
  if op == 'correlate':
    y = ufuncs.conj(y)
    if len(x) < len(y):
      x, y = y, x
      out_order = slice(None, None, -1)
  elif op == 'convolve':
    if len(x) < len(y):
      x, y = y, x
    y = flip(y)

  if mode == 'valid':
    padding = [(0, 0)]
  elif mode == 'same':
    padding = [(y.shape[0] // 2, y.shape[0] - y.shape[0] // 2 - 1)]
  elif mode == 'full':
    padding = [(y.shape[0] - 1, y.shape[0] - 1)]
  else:
    raise ValueError("mode must be one of ['full', 'same', 'valid']")

  result = lax_conv.conv_general_dilated(x[None, None, :], y[None, None, :], (1,),
                                         padding, precision=precision,
                                         preferred_element_type=preferred_element_type)
  return result[0, 0, out_order]

