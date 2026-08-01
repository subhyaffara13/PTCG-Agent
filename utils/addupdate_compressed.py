
def addupdate_compressed(ref: Ref, x: jax.Array, *, mask: jax.Array) -> None:
  """Performs a masked atomic add to a ref.

  See ``store_compressed`` for details on how the mask is used.
  """
  if not isinstance(ref, Ref):
    raise TypeError(f"ref must be an AbstractRef or TransformedRef, got {ref}")
  if not isinstance(ref, TransformedRef):
    ref = ref.at[...]  # pyrefly: ignore[bad-index]
  assert isinstance(ref, TransformedRef)
  flat_transforms, tree = jax.tree.flatten(ref.transforms)
  _ = swap_p.bind(
      ref.ref, x, *flat_transforms, mask, has_mask=True, tree=tree, add=True
  )
  return None

