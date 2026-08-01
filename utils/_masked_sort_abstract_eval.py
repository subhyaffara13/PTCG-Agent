
def _masked_sort_abstract_eval(keys, values, *maybe_mask, descending):
  del descending  # Unused.
  supported_shape = (sc_core.get_sparse_core_info().num_lanes,)
  if keys.dtype not in (jnp.uint32, jnp.int32, jnp.float32):
    raise NotImplementedError(
        f"sort_key_val: keys dtype {keys.dtype} should be uint32, int32 or"
        " float32")
  if keys.shape != supported_shape:
    raise ValueError(f"keys shape {keys.shape} must be {supported_shape}")
  if jnp.dtype(values.dtype).itemsize != 4:
    raise NotImplementedError(
        f"sort_key_val: values dtype {values.dtype} should be 32 bits")
  if values.shape != supported_shape:
    raise ValueError(f"values shape {values.shape} must be {supported_shape}")
  if maybe_mask:
    [mask] = maybe_mask
    if not jnp.issubdtype(mask.dtype, jnp.bool):
      raise TypeError(f"mask dtype {mask.dtype} is not boolean")
    if mask.shape != supported_shape:
      raise ValueError(f"mask shape {mask.shape} must be {supported_shape}")
  return keys, values, *maybe_mask

