
def remote_ref(
    ref: _Ref,
    device_id: jax.typing.ArrayLike,
    device_id_type: pallas_primitives.DeviceIdType = pallas_primitives.DeviceIdType.MESH,
) -> pallas_core.TransformedRef:
  """Translate memref to a symmetric memref on a peer device."""
  if not isinstance(ref, pallas_core.TransformedRef):
    if not isinstance(jax_core.typeof(ref), state_types.AbstractRef):
      raise TypeError("ref must be a reference")
    ref = pallas_core.TransformedRef(ref, transforms=())
  if any(isinstance(t, MulticastRef) for t in ref.transforms):
    raise ValueError("Can't make a multicast reference into a peer reference.")
  return pallas_core.TransformedRef(
      ref.ref, (*ref.transforms, PeerMemRef(device_id, device_id_type)),
  )

