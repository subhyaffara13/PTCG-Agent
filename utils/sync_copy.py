
def sync_copy(src_ref, dst_ref, *, add: bool = False) -> None:
  """Synchronously copies a PyTree of refs to another PyTree of refs."""
  if not jax.tree.leaves(src_ref):
    # No buffers to copy so skip the function.
    return

  @functools.partial(
      pl_primitives.run_scoped, sem=tpu_core.SemaphoreType.DMA(())
  )
  def _(sem):
    def _copy_start_or_wait(action, src_ref, dst_ref):
      descriptor = plm_primitives.make_async_copy(src_ref, dst_ref, sem)
      if action == "start":
        descriptor.start(add=add)
      elif action == "wait":
        descriptor.wait()
      else:
        raise ValueError(f"Unknown action: {action}")

    jax.tree.map(
        functools.partial(_copy_start_or_wait, "start"),
        src_ref,
        dst_ref,
    )
    jax.tree.map(
        functools.partial(_copy_start_or_wait, "wait"),
        src_ref,
        dst_ref,
    )


def sync_copy(src: REF | BufferedRef, dst: REF | BufferedRef, indices):
  """Perform a synchronous copy from src to dst."""
  bref: BufferedRef
  hbm_ref: REF
  if isinstance(src, BufferedRef):
    bref = src
    if isinstance(dst, BufferedRef):
      raise ValueError("Only one of src or dst can be a BufferedRef.")
    hbm_ref = dst
    copy_in = False
  else:
    if not isinstance(dst, BufferedRef):
      raise ValueError("One of src or dst must be a BufferedRef.")
    bref = dst
    hbm_ref = src
    copy_in = True
  window_ref = bref.current_ref
  if not bref.is_trivial_windowing:
    hbm_slice = bref.get_dma_slice(_ref_to_value_aval(hbm_ref), indices)
    bref_slice = bref._to_window_slice(hbm_slice)
    hbm_ref = hbm_ref.at[hbm_slice]
    window_ref = window_ref.at[bref_slice]
  if copy_in:
    tpu_helpers.sync_copy(hbm_ref, window_ref)
  else:
    tpu_helpers.sync_copy(window_ref, hbm_ref)

