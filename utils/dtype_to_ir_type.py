
def dtype_to_ir_type(dtype: core.bint | np.dtype | np.generic) -> ir.Type:
  if isinstance(dtype, core.bint):
    # TODO Support different-size underlying dtypes to take advantage of the
    # bound for packing?
    dtype = np.dtype(np.int32)
  assert isinstance(dtype, (np.dtype, np.generic)), type(dtype)
  dtype = np.dtype(dtype)
  try:
    ir_type_factory = _dtype_to_ir_type[dtype]
  except KeyError as err:
    raise TypeError(
        f"No dtype_to_ir_type handler for dtype: {dtype}") from err
  return ir_type_factory()


def dtype_to_ir_type(dtype: jax.typing.DTypeLike) -> ir.Type:
  dtype = jnp.dtype(dtype)
  if jnp.issubdtype(dtype, jnp.integer):
    # All integer types in Mosaic GPU are signless.
    return ir.IntegerType.get_signless(jnp.iinfo(dtype).bits)
  return mlir.dtype_to_ir_type(dtype)

