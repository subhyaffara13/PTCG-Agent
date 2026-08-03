from typing import Any

def _async_prefetch_lowering(
    ctx: lowering.LoweringRuleContext,
    ref,
    *flat_ref_transforms,
    ref_transforms_treedef,
    collective_axes,
    leader_tracked,
):
  ref_transforms = ref_transforms_treedef.unflatten(flat_ref_transforms)
  ref_transform_avals = ref_transforms_treedef.unflatten(ctx.avals_in[1:])
  copy_params = _extract_gmem_copy_params(
      ctx, ref_transforms, ref_transform_avals
  )
  collective = None
  if collective_axes is not None:
    collective = tuple(
        lowering._resolve_cluster_axis(ctx.module_ctx.axis_names, axis)
        for axis in collective_axes
    )

  if ctx.module_ctx.lowering_semantics == mgpu.LoweringSemantics.Lane:
    predicate_kwarg: dict[str, Any] = dict(
        predicate=ctx.module_ctx.single_lane_predicate
    )
    if gmem_slice := copy_params.get("gmem_slice", ()):
      first_idx = gmem_slice[0]
      # Gathers are a warpgroup-level collective and can't take a predicate.
      if isinstance(first_idx, mgpu.FragmentedArray) and first_idx.shape:
        predicate_kwarg = {}

    ctx.launch_ctx.async_prefetch(
        gmem_ref=ref,
        collective=collective,
        leader_tracked=leader_tracked,
        **copy_params,
        **predicate_kwarg,
    )
    return ()

  if "gmem_slice" not in copy_params:
    i32 = ir.IntegerType.get_signless(32)
    slice_lengths = ir.MemRefType(ref.type).shape
    indices = [mgpu.utils.c(0, i32)] * len(slice_lengths)
  else:
    indices, slice_lengths = _split_gmem_slice(copy_params["gmem_slice"])
  assert copy_params.get("swizzle") is None
  assert not copy_params.get("gmem_transform")
  if copy_params.get("gmem_peer_id", None) is not None:
    raise NotImplementedError(
        "GMEM refs with peer ids are not supported in warpgroup lowering."
    )
  mgpu.dialect.async_prefetch(
      ref, indices, slice_lengths, collective=ir.ArrayAttr.get([])
  )
  return ()

