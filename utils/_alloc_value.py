
def _alloc_value(
    aval: jax_core.AbstractValue | ShapedAbstractValue, *, ctx: LoweringRuleContext
) -> ir.Value:
  if isinstance(aval, state.AbstractRef):
    if jnp.issubdtype(aval.dtype, pallas_core.semaphore_dtype):
      assert aval.memory_space == SEMAPHORE
      memref_type = ctx.aval_to_ir_type(aval, memory_space=SEMAPHORE)
      return tpu.sem_alloc(memref_type)
    else:
      memref_type = ctx.aval_to_ir_type(
          aval, is_kernel_boundary=True, memory_space=aval.memory_space
      )
      assert isinstance(memref_type, ir.MemRefType)
      res = memref.alloca(memref_type, [], [])
      if pallas_core.poison_buffers_enabled():
        _poison_memref(res)
      return res
  elif isinstance(aval, tpu_core.AbstractSemaphore):
    memref_type = ctx.aval_to_ir_type(aval, memory_space=SEMAPHORE)
    return tpu.sem_alloc(memref_type)
  raise NotImplementedError(f"Cannot allocate {type(aval)}.")

