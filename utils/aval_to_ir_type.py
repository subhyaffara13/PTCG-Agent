
def aval_to_ir_type(ctx: ModuleContext, aval: core.AbstractValue) -> ir.Type:
  """Converts a JAX aval to a single MLIR IR type.

  Use only when ``aval`` is known to map to a single IR type. For opaque
  avals, use ``aval_to_ir_types`` instead.
  """
  ir_type = _aval_to_ir_types(ctx, aval)
  if isinstance(ir_type, ir.Type):
    return ir_type
  raise TypeError(f"Expected a single IR type, got {ir_type}")


def aval_to_ir_type(
    dynamic_shape_replacement_fn: DynamicShapeReplacementFn,
    aval,
    *,
    shape=None,
    memory_space: AnyMemorySpace | None = None,
    is_kernel_boundary: bool = False,
    allow_extended_types: bool = True,
    kernel_type: tpu_core.CoreType,
):
  if allow_extended_types and should_physicalize_dtype(aval.dtype):
    if isinstance(aval, state.AbstractRef):
      # pyrefly: ignore[bad-argument-type]
      inner_aval = _physical_aval(aval.inner_aval)
      physical_aval = aval.update(inner_aval=inner_aval)
    else:
      physical_aval = _physical_aval(aval)
    if shape is not None:
      shape = jax_core.physical_shape(shape, aval.dtype)
    return aval_to_ir_type(
        dynamic_shape_replacement_fn,
        aval=physical_aval,
        shape=shape,
        memory_space=memory_space,
        is_kernel_boundary=is_kernel_boundary,
        allow_extended_types=False,
        kernel_type=kernel_type,
    )
  if isinstance(aval, tpu_core.AbstractSemaphore):
    if aval.sem_type is tpu_core.SemaphoreType.DMA:
      sem_type = ir.Type.parse("!tpu.dma_semaphore")
    elif aval.sem_type is tpu_core.SemaphoreType.REGULAR:
      sem_type = ir.Type.parse("!tpu.semaphore")
    elif aval.sem_type is tpu_core.SemaphoreType.BARRIER:
      sem_type = ir.Type.parse("!tpu.semaphore")
    else:
      raise ValueError(f"Cannot allocate {aval.sem_type}.")
    memspace = _memory_space_to_mosaic_attribute(SEMAPHORE, kernel_type)
    return ir.MemRefType.get((), sem_type, memory_space=memspace)
  if isinstance(aval, state.AbstractRef):
    if shape is None:
      shape = aval.shape
    if memory_space is None:
      memory_space = aval.memory_space
    memspace = _memory_space_to_mosaic_attribute(memory_space, kernel_type)
    shape = dynamic_shape_replacement_fn(shape)
    return ir.MemRefType.get(shape,
      _dtype_to_ir_type(aval.dtype, is_kernel_boundary=True),
      memory_space=memspace)
  if isinstance(aval, jax_core.ShapedArray):
    if shape is None:
      shape = aval.shape
    if not shape:
      return _dtype_to_ir_type(
          aval.dtype, is_kernel_boundary=is_kernel_boundary)
    shape = dynamic_shape_replacement_fn(shape)
    return ir.VectorType.get(
        dynamic_shape_replacement_fn(shape),
        _dtype_to_ir_type(aval.dtype, is_kernel_boundary=is_kernel_boundary))
  raise NotImplementedError(aval)

