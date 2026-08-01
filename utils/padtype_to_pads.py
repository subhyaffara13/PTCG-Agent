
def padtype_to_pads(in_shape, filter_shape, window_strides, padding):
  if padding.upper() == 'SAME' or padding.upper() == 'SAME_LOWER':
    out_shape = np.ceil(np.true_divide(in_shape, window_strides)).astype(int)
    pad_sizes = [_max((out_size - 1) * stride + filter_size - in_size, 0)
                 for out_size, stride, filter_size, in_size
                 in zip(out_shape, window_strides, filter_shape, in_shape)]
    if padding.upper() == 'SAME':
      return [
          (pad_size // 2, pad_size - pad_size // 2) for pad_size in pad_sizes
      ]
    else:
      return [
          (pad_size - pad_size // 2, pad_size // 2) for pad_size in pad_sizes
      ]
  else:
    return [(0, 0)] * len(in_shape)


def padtype_to_pads(
    in_shape: Sequence[int] | np.ndarray,
    window_shape: Sequence[int] | np.ndarray,
    window_strides: Sequence[int] | np.ndarray,
    padding: str | PaddingType) -> list[tuple[int, int]]:
  """Convert a padding specification to a list of pad value pairs.

  This utility resolves abstract convolution padding modes into concrete
  per-dimension integer padding values based on the input and window geometry.

  Args:
    in_shape: Sequence of integers specifying the input spatial shape.
    window_shape: Sequence of integers specifying the kernel/window spatial shape.
    window_strides: Sequence of integers specifying the spatial strides.
    padding: Either a padding string (``'SAME'``, ``'SAME_LOWER'``, or ``'VALID'``)
      or a ``PaddingType`` enum value. Other values will result in an error.

  Returns:
    A list of ``(low, high)`` integer tuples, one for each spatial dimension,
    specifying the padding to apply before and after each dimension.

  Raises:
    RuntimeError: If ``padding`` is a string but not one of the supported values.
    TypeError: If ``padding`` is not a supported string or ``PaddingType`` value.

  Notes:
    - ``'VALID'``: Returns zero padding ``(0, 0)`` for all dimensions.
    - ``'SAME'``: Pads such that the output spatial shape is computed via
      ceiling division of ``in_shape`` by ``window_strides``. If the required
      padding amount is odd, the extra padding is added to the **end**
      (high side) of the dimension.
    - ``'SAME_LOWER'``: Similar to ``'SAME'``, but if the required padding
      amount is odd, the extra padding is added to the **start**
      (low side) of the dimension.
  """
  if isinstance(padding, str):
    try:
      padding = PaddingType[padding.upper()]
    except KeyError as err:
      raise RuntimeError(
        f"Unrecognized padding type: expected 'VALID', 'SAME', or 'SAME_LOWER', got {padding}."
      ) from err

  if padding in (PaddingType.SAME, PaddingType.SAME_LOWER):
    out_shape = _ceil_divide(in_shape, window_strides)
    pad_sizes = (core.max_dim(d, 0)
                 for d in (out_shape - 1) * window_strides +
                          window_shape - in_shape)
    if padding == PaddingType.SAME:
      pads = [
          (pad_size // 2, pad_size - pad_size // 2) for pad_size in pad_sizes
      ]
    else:
      pads = [
          (pad_size - pad_size // 2, pad_size // 2) for pad_size in pad_sizes
      ]
    # Avoids verbose numpy scalars in jaxprs.
    return tree_util.tree_map(lambda x: x.item() if isinstance(x, np.generic) else x, pads)
  elif padding == PaddingType.VALID:
    return [(0, 0)] * len(in_shape)
  else:
    raise TypeError(f"Unknown padding type: {padding}.")

