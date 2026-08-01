
def _dma_wait_to_lojax(*args, tree, device_id_type, insert_dummy_device: bool):
  del insert_dummy_device
  src_ref, dst_ref, dst_sem, src_sem, device_id = _dma_unflatten(tree, args)
  src_ref_aval = jax_core.typeof(_get_ref(src_ref))
  dst_ref_aval = jax_core.typeof(_get_ref(dst_ref))
  if not (src_ref_aval.is_high and dst_ref_aval.is_high):
    raise NotImplementedError("dma_wait not implemented in LoJAX yet.")
  dst_sem_aval = jax_core.typeof(_get_ref(dst_sem))
  if dst_sem_aval.is_high:
    raise NotImplementedError("dma_wait not implemented in LoJAX yet.")
  if _get_ref(src_sem) is not None:
    if jax_core.typeof(_get_ref(src_sem)).is_high:
      raise NotImplementedError("dma_wait not implemented in LoJAX yet.")
  # LoJAX expects TransformedRef if passed that way.
  src_ref_aval.inner_aval.dma_wait(
      src_ref,
      dst_ref,
      src_sem,
      dst_sem,
      device_id=device_id,
      device_id_type=device_id_type,
  )
  return []

