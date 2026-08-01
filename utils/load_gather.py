
def load_gather(
    ref: Ref, indices: Sequence[jax.Array], *, mask: jax.Array | None = None
) -> jax.Array:
  """Gathers an array from a ref.

  Args:
    ref: The ref in ``VMEM`` to gather from.
    indices: A sequence of 1D arrays, one for each dimension of ``ref``. Each
      array specifies an index for that dimension. All arrays must have the same
      size.
    mask: An optional boolean array, which specifies which elements to load. If
      ``None``, all elements are loaded.

  Returns:
    The gathered array.
  """
  ref, transforms = state_primitives.get_ref_and_transforms(
      ref, None, "load_gather"
  )
  flat_args, tree = jax.tree.flatten((ref, transforms, indices, mask))
  return gather_p.bind(*flat_args, tree=tree)

