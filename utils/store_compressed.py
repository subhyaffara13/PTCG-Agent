
def store_compressed(ref: Ref, x: jax.Array, *, mask: jax.Array) -> None:
  """Performs a compressed masked store to a ref.

  Elements from ``x`` where ``mask`` is ``True`` are placed into ``ref``.
  The elements are written to ``ref`` sequentially, meaning the i-th ``True``
  value in ``mask`` corresponds to writing to ``ref[i]``.

  For example, if the mask is ``[True, False, True, True]``, the elements
  ``x[0]``, ``x[2]``, and ``x[3]`` are written to ``ref[0]``, ``ref[1]``, and
  ``ref[2]`` respectively.

  Args:
    ref: The ref to store into.
    x: The array to store. Must have the same shape as ``ref``.
    mask: A boolean mask specifying which elements from ``x`` to store.
  """
  if not isinstance(ref, Ref):
    raise TypeError(f"ref must be an AbstractRef or TransformedRef, got {ref}")
  if not isinstance(ref, TransformedRef):
    ref = ref.at[...]  # pyrefly: ignore[bad-index]
  assert isinstance(ref, TransformedRef)
  flat_transforms, tree = jax.tree.flatten(ref.transforms)
  _ = swap_p.bind(
      ref.ref,
      x,
      *flat_transforms,
      mask,
      has_mask=True,
      tree=tree,
      add=False,
  )
  return None

