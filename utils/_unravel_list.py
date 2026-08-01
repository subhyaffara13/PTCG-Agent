
def _unravel_list(
  sizes: Sizes,
  shapes: Shapes,
  from_dtypes: tuple[np.dtype, ...],
  to_dtype: np.dtype,
  arr: Array,
) -> list[Array]:
  arr_dtype = dtypes.dtype(arr)
  if arr_dtype != to_dtype:
    raise TypeError(
      f"unravel function given array of dtype {arr_dtype}, "
      f"but expected dtype {to_dtype}"
    )
  chunks = lax.split(arr, sizes)
  return [
    lax._convert_element_type(
      chunk.reshape(shape), dtype, warn_on_complex_to_real_cast=False
    )
    for chunk, shape, dtype in zip(chunks, shapes, from_dtypes)
  ]

