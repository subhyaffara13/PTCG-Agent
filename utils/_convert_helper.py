
def _convert_helper(x: Array, *, to_dtype: jnp.dtype) -> Array:
  # Helper function for dtype conversion
  from_dtype = x.dtype
  from_bitwidth = dtypes.itemsize_bits(from_dtype)
  to_bitwidth = dtypes.itemsize_bits(to_dtype)
  if from_dtype == jnp.bool_:
    x = x.astype(jnp.int32)
    return _convert_helper(x, to_dtype=to_dtype)
  if to_dtype == jnp.bool_:
    # Lower float32 or (u)int32 -> bool to cmp neq %in, 0
    # TODO(apaszke,mvoz): Move the upcasts for cmpi to the Mosaic canonicalizer.
    if jnp.issubdtype(from_dtype, jnp.floating):
      if from_bitwidth < 32:
        x = x.astype(jnp.float32)
    elif jnp.issubdtype(from_dtype, jnp.integer):
      if from_bitwidth < 32:
        x = x.astype(jnp.int32)
    return x != jnp.asarray(0, dtype=x.dtype)
  if jnp.issubdtype(from_dtype, jnp.signedinteger):
    if from_bitwidth < 32:
      x = x.astype(jnp.int32)
    if jnp.issubdtype(to_dtype, jnp.floating) and to_bitwidth < 32:
      x = x.astype(jnp.float32)
    return x.astype(to_dtype)
  if jnp.issubdtype(from_dtype, jnp.unsignedinteger):
    if from_bitwidth < 32:
      x = x.astype(jnp.uint32)
    # unsigned -> float is unsupported. We fall through and raise at the bottom.
    if not jnp.issubdtype(to_dtype, jnp.floating):
      return x.astype(to_dtype)
  raise NotImplementedError(f"Unsupported cast: {from_dtype} -> {to_dtype}")

