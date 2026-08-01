
def _dma_start_to_lojax(*args, tree, device_id_type, priority, add):
  src_ref, dst_ref, dst_sem, src_sem, device_id = _dma_unflatten(tree, args)
  src_ref_aval = jax_core.typeof(_get_ref(src_ref))
  dst_ref_aval = jax_core.typeof(_get_ref(dst_ref))
  if not (src_ref_aval.is_high and dst_ref_aval.is_high):
    raise NotImplementedError("dma_start not implemented in LoJAX yet.")
  dst_sem_aval = jax_core.typeof(_get_ref(dst_sem))
  if dst_sem_aval.is_high:
    raise NotImplementedError("dma_start not implemented in LoJAX yet.")
  if _get_ref(src_sem) is not None:
    if jax_core.typeof(_get_ref(src_sem)).is_high:
      raise NotImplementedError("dma_start not implemented in LoJAX yet.")
  src_ref_aval.inner_aval.dma_start(
      src_ref,
      dst_ref,
      src_sem,
      dst_sem,
      device_id=device_id,
      priority=priority,
      device_id_type=device_id_type,
      add=add,
  )
  return []

