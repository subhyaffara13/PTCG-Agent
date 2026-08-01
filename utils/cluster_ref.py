
def cluster_ref(
    ref: _Ref,
    block_id: dict[jax_core.AxisName, Any],
) -> pallas_core.TransformedRef:
  """Translate memref to a peer memref in the cluster."""
  if not isinstance(ref, pallas_core.TransformedRef):
    if not isinstance(jax_core.typeof(ref), state_types.AbstractRef):
      raise TypeError("ref must be a reference")
    ref = pallas_core.TransformedRef(ref, transforms=())
  dims = tuple(block_id.keys())
  idxs = tuple(block_id.values())
  return pallas_core.TransformedRef(
      ref.ref, (*ref.transforms, ClusterRefTransform(dims, idxs)),
  )

