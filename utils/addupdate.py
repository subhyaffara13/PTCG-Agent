
def addupdate(ref: Ref, x: jax.Array) -> None:
  """Performs an atomic add to a ref.

  Args:
    ref: The ref to store into.
    x: The array to store. Must have the same shape as ``ref``.
  """
  if not isinstance(ref, Ref):
    raise TypeError(f"ref must be an AbstractRef or TransformedRef, got {ref}")
  if not isinstance(ref, TransformedRef):
    ref = ref.at[...]  # pyrefly: ignore[bad-index]
  assert isinstance(ref, TransformedRef)
  flat_transforms, tree = jax.tree.flatten(ref.transforms)
  _ = swap_p.bind(
      ref.ref, x, *flat_transforms, has_mask=False, tree=tree, add=True
  )
  return None

