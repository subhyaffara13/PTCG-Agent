
def _pad_linear_ramp(array: Array, pad_width: PadValue[int],
                     end_values: PadValue[ArrayLike]) -> Array:
  for axis in range(np.ndim(array)):
    edge_before = lax_slicing.slice_in_dim(array, 0, 1, axis=axis)
    edge_after = lax_slicing.slice_in_dim(array, -1, None, axis=axis)
    ramp_before = array_creation.linspace(
        start=end_values[axis][0],
        stop=edge_before.squeeze(axis), # Dimension is replaced by linspace
        num=pad_width[axis][0],
        endpoint=False,
        dtype=array.dtype,
        axis=axis
    )
    ramp_before = lax._convert_element_type(
        ramp_before, weak_type=dtypes.is_weakly_typed(array))
    ramp_after = array_creation.linspace(
        start=end_values[axis][1],
        stop=edge_after.squeeze(axis), # Dimension is replaced by linspace
        num=pad_width[axis][1],
        endpoint=False,
        dtype=array.dtype,
        axis=axis
    )
    ramp_after = lax._convert_element_type(
        ramp_after, weak_type=dtypes.is_weakly_typed(array))

    # Reverse linear space in appropriate dimension
    ramp_after = flip(ramp_after, axis)

    array = lax.concatenate([ramp_before, array, ramp_after], dimension=axis)
  return array

