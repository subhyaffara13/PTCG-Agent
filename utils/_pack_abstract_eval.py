
def _pack_abstract_eval(a, b, *, format, preferred_element_type):
  if a.shape != b.shape:
    raise ValueError(
        f"Packed arrays must have the same shape, got {a.shape} and {b.shape}"
    )
  if a.ndim != 1:
    raise ValueError(f"Packed arrays must be 1-D, got {a.ndim}")
  if a.dtype != b.dtype:
    raise TypeError(
        f"Packed arrays must have the same dtype, got {a.dtype} and {b.dtype}"
    )
  if preferred_element_type is None:
    match a.dtype:
      case jnp.float32:
        packed_dtype = jnp.bfloat16
      case jnp.int32:
        packed_dtype = jnp.int16
      case _:
        # TODO(slebedev): Support more types.
        raise NotImplementedError(
            f"Only packing of float32 and int32 is supported, got {a.dtype}"
        )
  else:
    packed_bw = dtypes.itemsize_bits(a.dtype) // 2
    if dtypes.itemsize_bits(preferred_element_type) != packed_bw:
      raise ValueError(
          f"preferred_element_type= must have bitwidth {packed_bw}, got"
          f" {dtypes.itemsize_bits(preferred_element_type)}"
      )
    packed_dtype = preferred_element_type

  match format:
    case PackFormat.INTERLEAVED:
      packed_shape = (2 * a.size,)
    case PackFormat.COMPRESSED:
      packed_shape = (a.size, 2)
    case _:
      raise TypeError(f"Unexpected format: {format}")
  return jax_core.ShapedArray(packed_shape, packed_dtype)

