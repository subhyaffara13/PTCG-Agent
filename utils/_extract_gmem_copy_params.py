
def _extract_gmem_copy_params(
    ctx, transforms, transform_avals, supports_multicast=False
):
  if not transforms:
    return {}
  peer_id = None
  indexers = []
  for transform, transform_aval in zip(
      transforms, transform_avals, strict=True
  ):
    if isinstance(transform, gpu_core.PeerMemRef):
      peer_id = lowering._device_id_to_logical(
          ctx,
          transform.device_id,
          transform.device_id_type,
          transform_aval.device_id,
      )
      peer_id = lowering._ensure_ir_value(peer_id, jnp.int32)
      continue
    elif isinstance(transform, gpu_core.MulticastRef):
      if not supports_multicast:
        raise ValueError(
            "Multicast refs are not supported by this primitive."
        )
      if (mesh_info := ctx.module_ctx.mesh_info) is None:
        raise ValueError(
            "JAX device mesh is required by multicast copies, but not defined."
            " Use jax.set_mesh."
        )
      if set(transform.collective_axes) != set(mesh_info.axis_names):
        raise NotImplementedError(
            "Only collective_axes that include all JAX device mesh  axes are"
            f" supported, but got {transform.collective_axes}. Make sure to"
            f" pass collective_axes={mesh_info.axis_names}"
        )
      peer_id = mgpu.GLOBAL_BROADCAST
      continue
    elif isinstance(transform, indexing.NDIndexer):
      indexers.append(transform)
    else:
      raise NotImplementedError(
          "Non-indexing transforms on GMEM refs are not implemented.")
  if indexers:
    indexer = lowering.merge_indexers(indexers)
    gmem_slice = lowering._ndindexer_indices(indexer, allow_arrays=True)
  else:
    gmem_slice = ()
  return dict(
      gmem_slice=gmem_slice,
      gmem_peer_id=peer_id,
  )

