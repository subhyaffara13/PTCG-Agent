
def _unpack_abstract_eval(ab, *, format, preferred_element_type):
  match format:
    case PackFormat.INTERLEAVED:
      if ab.ndim != 1 or ab.size % 2 != 0:
        raise ValueError(
            "Interleaved unpack requires a 1-D array with an even size, got"
            f" {ab.shape}"
        )
    case PackFormat.COMPRESSED:
      if ab.ndim != 2 or ab.shape[1] != 2:
        raise ValueError(
            "Compressed unpack requires an array with shape (N, 2), got"
            f" {ab.shape}"
        )
  if preferred_element_type is None:
    match ab.dtype:
      case jnp.bfloat16:
        unpacked_dtype = jnp.float32
      case jnp.int16:
        unpacked_dtype = jnp.int32
      case _:
        # TODO(slebedev): Support more types.
        raise NotImplementedError(
            f"Only unpacking of bloat16 and int16 is supported, got {ab.dtype}"
        )
  else:
    unpacked_bw = dtypes.itemsize_bits(ab.dtype) * 2
    if dtypes.itemsize_bits(preferred_element_type) != unpacked_bw:
      raise ValueError(
          f"preferred_element_type= must have bitwidth {unpacked_bw}, got"
          f" {dtypes.itemsize_bits(preferred_element_type)}"
      )
    unpacked_dtype = preferred_element_type
  return (jax_core.ShapedArray((ab.size // 2,), unpacked_dtype),) * 2

