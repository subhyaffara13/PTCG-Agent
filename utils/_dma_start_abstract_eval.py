
def _dma_start_abstract_eval(*args, tree, device_id_type, priority, add):
  if priority < 0:
    raise ValueError(f"DMA start priority must be non-negative: {priority}")
  src_ref_aval, dst_ref_aval, dst_sem_aval, src_sem_aval, device_id_aval = (
      _dma_unflatten(tree, args)
  )
  if not all(
      isinstance(x, (state.AbstractRef, state.TransformedRef))
      for x in [src_ref_aval, dst_ref_aval, dst_sem_aval]
  ):
    raise ValueError(
        "DMA source/destination/semaphore arguments must be Refs.")
  dst_sem_shape = dst_sem_aval.shape
  if dst_sem_shape:
    raise ValueError(
        f"Cannot signal on a non-()-shaped semaphore: {dst_sem_shape}"
    )
  if src_sem_aval is not None:
    if not isinstance(src_sem_aval, (state.AbstractRef, state.TransformedRef)):
      raise ValueError("DMA source semaphore must be a Ref.")
    src_sem_shape = src_sem_aval.shape
    if src_sem_shape:
      raise ValueError(
          f"Cannot signal on a non-()-shaped semaphore: {src_sem_shape}"
      )
  return [], _get_dma_effects(
      src_ref_aval,
      dst_ref_aval,
      dst_sem_aval,
      src_sem_aval,
      device_id_aval,
      device_id_type,
  )

