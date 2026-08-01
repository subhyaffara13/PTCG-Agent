
def _dma_wait_abstract_eval(*args, tree, device_id_type, insert_dummy_device: bool):
  src_ref_aval, dst_ref_aval, dst_sem_aval, src_sem_aval, device_id_aval = (
      _dma_unflatten(tree, args)
  )
  if not isinstance(dst_sem_aval, (state.AbstractRef, state.TransformedRef)):
    raise ValueError("Expected the destination semaphore to be a reference")
  allowed_semaphore_types = {
      tpu_core.dma_semaphore,
      pl_core.SEMAPHORE_INTERPRET_DTYPE,
  }
  if not any(
      jnp.issubdtype(dst_sem_aval.dtype, t) for t in allowed_semaphore_types
  ):
    raise ValueError(
        "dma_wait requires a DMA semaphore, but got a regular semaphore."
        " Use pl.semaphore_wait() instead."
    )
  return [], _get_dma_effects(
      src_ref_aval,
      dst_ref_aval,
      dst_sem_aval,
      src_sem_aval,
      device_id_aval,
      device_id_type,
  )

