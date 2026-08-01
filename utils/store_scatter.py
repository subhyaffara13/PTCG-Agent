
def store_scatter(
    ref: Ref,
    indices: Sequence[jax.Array],
    x: jax.Array,
    *,
    mask: jax.Array | None = None,
) -> None:
  """Scatters an array to a ref.

  Args:
    ref: The ref in ``VMEM`` to scatter to.
    indices: A sequence of 1D arrays, one for each dimension of ``ref``. Each
      array specifies an index for that dimension. All arrays must have the same
      size.
    val: The array to store.
    mask: An optional boolean array, which specifies which elements to store. If
      ``None``, all elements are stored.
  """
  if not indices:
    raise ValueError("Indices must not be empty")
  ref, transforms = state_primitives.get_ref_and_transforms(
      ref, None, "store_scatter"
  )
  flat_args, tree = jax.tree.flatten((ref, transforms, indices, x, mask))
  _ = scatter_p.bind(*flat_args, tree=tree, add=False)
  return None

