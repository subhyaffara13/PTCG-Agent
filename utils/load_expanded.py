
def load_expanded(ref: Ref, *, mask: jax.Array) -> jax.Array:
  """Performs and expanded masked load from a ref.

  Elements from ``ref`` are placed into positions where ``mask`` is ``True``.
  The elements are taken from ``ref`` sequentially, meaning that the i-th
  ``True`` value in ``mask`` corresponds to accessing ``ref[i]``. The result is
  expanded into the shape of the ``mask``.

  For example, if the mask is ``[True, False, True, True]``, the result is
  ```[ref[0], <?>,  ref[2], ref[3]]``, where ``<?>`` is an undefined value.

  Args:
    ref: The ref to load from.
    mask: A boolean mask specifying which elements to load into.

  Returns:
    The loaded array, with the same shape as the mask. No assumptions can be
    made about the elements at the indices where the mask is ``False``.
  """
  if not isinstance(ref, Ref):
    raise TypeError(f"ref must be an AbstractRef or TransformedRef, got {ref}")
  if not isinstance(ref, TransformedRef):
    ref = ref.at[...]  # pyrefly: ignore[bad-index]
  assert isinstance(ref, TransformedRef)
  flat_transforms, tree = jax.tree.flatten(ref.transforms)
  return load_p.bind(ref.ref, *flat_transforms, mask, has_mask=True, tree=tree)

