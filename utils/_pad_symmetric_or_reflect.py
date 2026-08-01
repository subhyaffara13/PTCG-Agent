
def _pad_symmetric_or_reflect(array: Array, pad_width: PadValue[int],
                              mode: str, reflect_type: str) -> Array:
  assert mode in ("symmetric", "reflect")
  assert reflect_type in ("even", "odd")

  for i in range(np.ndim(array)):
    axis_size = array.shape[i]
    if axis_size == 0:
      _check_no_padding(pad_width[i], mode)
      continue
    if pad_width[i][0] == 0 and pad_width[i][1] == 0:
      continue

    def build_padding(array, padding, before):
      if before:
        edge = lax_slicing.slice_in_dim(array, 0, 1, axis=i)
      else:
        edge = lax_slicing.slice_in_dim(array, -1, None, axis=i)

      # Try to give nicer error messages for unsupported shape polymorphic uses
      shape_poly_error_msg = lambda: (
          "Shape polymorphism is supported for jnp.pad with 'reflect' or "
          "'symmetric' padding mode only when it is possible to determine "
          f"at lowering time that the axis size (= {axis_size}) is larger than 1 "
          f"and larger or equal than the padding length (= {padding}). "
          f"Error while handling {'left' if before else 'right'} padding on axis {i}.")
      try:
        # We check that we can determine all comparisons.
        offset = 1 if (mode == "reflect" and axis_size > 1) else 0
        has_poly_dim = not core.is_constant_shape((axis_size, padding))
        # For shape polymorphism, ensure the loop below ends after 1 iteration
        if has_poly_dim and not (axis_size > 1 and axis_size - offset >= padding):
          raise ValueError(shape_poly_error_msg())
      except core.InconclusiveDimensionOperation as e:
        raise ValueError(shape_poly_error_msg()) from e

      while padding > 0:
        curr_pad = min(padding, axis_size - offset)
        padding -= curr_pad
        if has_poly_dim: assert padding == 0

        if before:
          start = offset
          stop = offset + curr_pad
        else:
          start = -(curr_pad + offset)
          stop = None if (mode == "symmetric" or axis_size == 1) else -1

        x = lax_slicing.slice_in_dim(array, start, stop, axis=i)
        x = flip(x, axis=i)

        if reflect_type == 'odd':
          x = 2 * edge - x
          if axis_size > 1:
            if before:
              edge = lax_slicing.slice_in_dim(x, 0, 1, axis=i)
            else:
              edge = lax_slicing.slice_in_dim(x, -1, None, axis=i)

        if before:
          array = lax.concatenate([x, array], dimension=i)
        else:
          array = lax.concatenate([array, x], dimension=i)
      return array

    array = build_padding(array, pad_width[i][0], before=True)
    array = build_padding(array, pad_width[i][1], before=False)
  return array

