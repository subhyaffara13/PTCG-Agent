
def _dtype_to_ir_type(dtype: DTypeLike,
                      is_kernel_boundary: bool = False) -> ir.Type:
  if jnp.issubdtype(dtype, pallas_core.semaphore_dtype):
    if jnp.issubdtype(dtype, tpu_core.dma_semaphore):
      return ir.Type.parse("!tpu.dma_semaphore")
    elif jnp.issubdtype(dtype, pallas_core.semaphore):
      return ir.Type.parse("!tpu.semaphore")
    elif jnp.issubdtype(dtype, pallas_core.barrier_semaphore):
      return ir.Type.parse("!tpu.semaphore")
    else:
      raise NotImplementedError
  if jnp.issubdtype(dtype, dtypes.extended):
    raise NotImplementedError(f"Extended dtype {dtype} is unsupported.")
  if is_kernel_boundary and jnp.issubdtype(dtype, jnp.bool):
    dtype = BOOL_MEMREF_TYPE
  # TODO(justinfu): Remove after mosaic supports unsigned types.
  # This conversion makes mosaic interpret all unsigned types as signed types.
  type = mlir.dtype_to_ir_type(jnp.dtype(dtype))
  if isinstance(type, ir.IntegerType):
    return ir.IntegerType.get_signless(type.width)
  else:
    return type


def _dtype_to_ir_type(dtype: jax.typing.DTypeLike) -> ir.Type:
  dtype = jnp.dtype(dtype)
  if jnp.issubdtype(dtype, np.integer):
    # All integer types in Triton are signless.
    return ir.IntegerType.get_signless(dtype.itemsize * 8)
  return mlir.dtype_to_ir_type(dtype)

