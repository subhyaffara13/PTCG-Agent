
def _async_store_smem_abstract_eval(
    src,
    ref,
    barrier,
    cluster_idx,
    *flat_transforms_avals,
    ref_transforms_treedef,
    barrier_transforms_treedef,
    **_,
):
  del cluster_idx  # Unused.
  _check_ref(ref, "ref", gpu_core.SMEM)
  _check_ref(barrier, "barrier", gpu_core.SMEM)
  flat_ref_transforms_avals, flat_barrier_transforms_avals = util.split_list(
      flat_transforms_avals,
      [ref_transforms_treedef.num_leaves],
  )
  ref_transform_avals = ref_transforms_treedef.unflatten(
      flat_ref_transforms_avals
  )
  barrier_transform_avals = barrier_transforms_treedef.unflatten(
      flat_barrier_transforms_avals
  )
  transformed_ref = pallas_core.TransformedRef(ref, ref_transform_avals)
  if src.shape != transformed_ref.shape:
    raise TypeError(
        f"The stored value has shape {src.shape}, but the target reference has"
        f" shape {transformed_ref.shape}"
    )
  if src.dtype != transformed_ref.dtype:
    raise TypeError(
        f"The stored value has dtype {src.dtype}, but the target reference has"
        f" dtype {transformed_ref.dtype}"
    )
  transformed_barrier = pallas_core.TransformedRef(barrier, barrier_transform_avals)
  if transformed_barrier.size != 1:
    raise TypeError(
        "Expected a single barrier, got a barrier reference with shape"
        f" {transformed_barrier.shape}"
    )

  effs = {gpu_core._memory_effect, state.WriteEffect(1)}
  return (), effs

