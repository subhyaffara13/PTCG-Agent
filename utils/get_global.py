
def get_global(result: _ods_ir.Type, name: _Union[str, _ods_ir.FlatSymbolRefAttr], *, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> _ods_ir.OpResult[_ods_ir.MemRefType]:
  return GetGlobalOp(result=result, name=name, loc=loc, ip=ip).result


def get_global(what: pallas_core.ScratchShape) -> jax_typing.Array:
  """Returns a global reference that persists across all kernel invocations.

  Each call to ``get_global`` returns a different and unique reference, but one that
  is stable across invocations of the kernel body.

  Args:
    what: The reference type to allocate. Each backend has its own set of
      reference types (e.g., :class:`jax.experimental.pallas.mosaic_gpu.SemaphoreType` for GPU).

  Example::

    sem_ref = pl.get_global(plgpu.SemaphoreType.REGULAR)
    pl.semaphore_signal(sem_ref)
    pl.semaphore_wait(sem_ref)
  """
  ref_aval = what.get_ref_aval()
  return get_global_p.bind(what=ref_aval)

