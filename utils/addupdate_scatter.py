
def addupdate_scatter(
    ref: Ref,
    indices: Sequence[jax.Array],
    x: jax.Array,
    *,
    mask: jax.Array | None = None,
) -> None:
  """Scatters an array to a ref atomically adding to existing values."""
  if not indices:
    raise ValueError("Indices must not be empty")
  ref, transforms = state_primitives.get_ref_and_transforms(
      ref, None, "store_scatter"
  )
  flat_args, tree = jax.tree.flatten((ref, transforms, indices, x, mask))
  _ = scatter_p.bind(*flat_args, tree=tree, add=True)

