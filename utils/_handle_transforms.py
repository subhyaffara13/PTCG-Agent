from typing import Any

def _handle_transforms(
    ctx: LoweringRuleContext,
    ref_aval: state_types.AbstractRef,
    ref: RefOrTmemType,
    transform_avals: Sequence[state_types.Transform],
    transforms: Sequence[state_types.Transform],
    *,
    handle_transposes=True,
    handle_reshapes=True,
    allow_peer_refs=False,
    allow_multicast_refs=False,
) -> tuple[
    RefOrTmemType, state_types.AbstractRef, Sequence[state_types.Transform]
]:
  # Before we handle other transforms, we resolve any possible leading
  # aliasing transform.
  ref, ref_aval, transform_avals, transforms = _extract_aliased_ref(
      ref,
      ref_aval,
      transform_avals,
      transforms,
      ctx.module_ctx.lowering_semantics,
  )

  if ctx.module_ctx.lowering_semantics == mgpu.LoweringSemantics.Warpgroup:
    # We only bubble up transforms here to verify that all the specified
    # transforms can be commuted correctly with the BlockSpec transforms.
    _bubble_up_transforms_for_lowering(
        ctx,
        ref_aval,
        transforms,
        transform_avals,
        handle_transposes=False,
        handle_reshapes=handle_reshapes,
    )

    spec_transforms = []
    num_block_spec_transforms = 0
    for t in transforms:
      if isinstance(t, (gpu_core.UntilingTransform, gpu_core.UnswizzleRef)):
        spec_transforms = [t.undo(ref_aval)] + spec_transforms
        ref_aval = cast(state_types.AbstractRef, t.transform_type(ref_aval))
        num_block_spec_transforms += 1
      else:
        break
    assert isinstance(ref, ir.Value)
    if spec_transforms:
      transforms_attr = ir.ArrayAttr.get([
          gpu_core.to_transform_attr(t) for t in spec_transforms
      ])
      ref = mgpu.dialect.with_transforms(_reinterpret_cast(ref, ref_aval), transforms_attr)
      transforms = transforms[num_block_spec_transforms:]
      transform_avals = transform_avals[num_block_spec_transforms:]
      if any(isinstance(t, (gpu_core.UntilingTransform, gpu_core.UnswizzleRef)) for t in transforms):
        raise ValueError("Unexpected untiling or unswizzle transform found in "
                         f"remaining transforms: {transforms}.")

  (
      bubbled_up_transforms,
      bubbled_up_transform_avals,
      remaining_transforms,
      _,
  ) = _bubble_up_transforms_for_lowering(
      ctx,
      ref_aval,
      transforms,
      transform_avals,
      handle_transposes=handle_transposes,
      handle_reshapes=handle_reshapes,
  )

  transformed_ref: Any = ref
  peer_device_id = None
  is_multicast = False
  cluster_dim = None
  cluster_idx = None

  for t_aval, t in zip(bubbled_up_transform_avals, bubbled_up_transforms):
    match t:
      case indexing.NDIndexer() as indexer:
        assert isinstance(t_aval, indexing.NDIndexer)
        if t_aval.int_indexer_shape:
          raise NotImplementedError("int_indexer_shape non-empty")
        indices = _ndindexer_indices(indexer)
        if (
            isinstance(transformed_ref, tcgen05.TMEMRef)
            and ctx.module_ctx.lowering_semantics == mgpu.LoweringSemantics.Lane
        ):
          transformed_ref = transformed_ref.slice(*indices)
        else:
          transformed_ref = mgpu_utils.memref_slice(transformed_ref, indices)
        ref_aval = t_aval.transform_type(ref_aval)
      case TransposeTransform() as t:
        assert handle_transposes
        if isinstance(transformed_ref, tcgen05.TMEMRef):
          raise ValueError("TMEM transpose not allowed.")
        transformed_ref = mgpu.memref_transpose(
            transformed_ref, t.permutation
        )
        ref_aval = t_aval.transform_type(ref_aval)  # pyrefly: ignore [bad-assignment]
      case ReshapeTransform() as t:
        assert handle_reshapes
        if isinstance(transformed_ref, tcgen05.TMEMRef):
          raise ValueError("TMEM reshape not allowed.")
        transformed_ref = mgpu.memref_reshape(transformed_ref, t.shape)
        ref_aval = t_aval.transform_type(ref_aval)  # pyrefly: ignore [bad-assignment]
      case gpu_core.PeerMemRef(device_id, device_id_type):
        assert isinstance(t_aval, gpu_core.PeerMemRef)
        peer_device_id = _device_id_to_logical(
            ctx, device_id, device_id_type, t_aval.device_id
        )
      case gpu_core.MulticastRef(_):
        if not allow_multicast_refs:
          raise NotImplementedError(
              "Multicast references are not allowed in the lowering of this"
              " primitive."
          )
        is_multicast = True
      case gpu_core.ClusterRefTransform(dims, idxs):
        if len(dims) != 1:
          raise NotImplementedError(
              "Only overriding a single cluster axis is supported for now."
          )
        cluster_dim = _resolve_cluster_axis(ctx.module_ctx.axis_names, dims[0])
        cluster_idx = _as_index(idxs[0])
      case _:
        raise AssertionError(
            f"Transform {t} has no defined lowering rule."
        )

  if cluster_dim is not None:
    assert cluster_idx is not None
    if ctx.module_ctx.lowering_semantics == mgpu.LoweringSemantics.Warpgroup:
      i32 = ir.IntegerType.get_signless(32)
      kwargs = dict(x=None, y=None, z=None)
      kwargs[cluster_dim.name] = arith_dialect.index_cast(i32, cluster_idx)
      transformed_ref = mgpu.dialect.get_cluster_ref(transformed_ref, **kwargs)
    else:
      transformed_ref = mgpu.get_cluster_ref(
          transformed_ref, cluster_dim, cluster_idx, generic=False
      )
  if peer_device_id is not None:
    assert not is_multicast
    if not allow_peer_refs:
      raise NotImplementedError(
          "Peer device references are not allowed in the lowering of this"
          " primitive."
      )
    transformed_ref = ctx.launch_ctx.to_remote(
        transformed_ref, _ensure_ir_value(peer_device_id, jnp.int32)
    )
  if is_multicast:
    transformed_ref = ctx.launch_ctx.to_remote_multicast(transformed_ref)
  assert isinstance(ref_aval, state_types.AbstractRef)
  return transformed_ref, ref_aval, remaining_transforms

