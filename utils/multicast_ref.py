
def multicast_ref(
    ref: _Ref,
    collective_axes: Hashable | tuple[Hashable, ...],
) -> pallas_core.TransformedRef:
  """Return a multicast reference for cross-device operations.

  Args:
    ref: The reference to transform.
    collective_axes: The JAX mesh axes indicating the devices to operate on.
  """
  if not isinstance(collective_axes, tuple):
    collective_axes = (collective_axes,)
  if not isinstance(ref, pallas_core.TransformedRef):
    if not isinstance(jax_core.typeof(ref), state_types.AbstractRef):
      raise TypeError("ref must be a reference")
    ref = pallas_core.TransformedRef(ref, transforms=())
  if any(isinstance(t, PeerMemRef) for t in ref.transforms):
    raise ValueError("Can't make a peer reference into a multicast reference.")
  return pallas_core.TransformedRef(
      ref.ref, (*ref.transforms, MulticastRef(collective_axes)),
  )

