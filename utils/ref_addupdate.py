
def ref_addupdate(
    ref: core.Ref | TransformedRef,
    idx: Indexer | tuple[Indexer, ...] | None,
    x: ArrayLike | HijaxType,
) -> None:
  """Add to an element in an Ref in-place.

  This is analogous to ``ref[idx] += value`` for a NumPy array ``ref`` and
  NumPy-style indexer ``idx``. However, for an Ref ``ref``, executing
  ``ref[idx] += value`` actually performs a ``ref_get``, add, and ``ref_set``,
  so using this function can be more efficient under autodiff. For more on
  mutable array refs, refer to the `Ref guide`_.

  Args:
    ref: a :class:`jax.ref.Ref` object. On return, the buffer will be
      mutated by this operation.
    idx: a NumPy-style indexer
    x: a :class:`jax.Array` object (note, not a :class:`jax.ref.Ref`)
      containing the values to add at the specified indices.

  Returns:
    None

  Examples:
    >>> import jax
    >>> ref = jax.new_ref(jax.numpy.arange(5))
    >>> jax.ref.addupdate(ref, 2, 10)
    >>> ref
    Ref([ 0,  1, 12,  3,  4], dtype=int32)

    Equivalent operation via indexing syntax:

    >>> ref = jax.new_ref(jax.numpy.arange(5))
    >>> ref[2] += 10
    >>> ref
    Ref([ 0,  1, 12,  3,  4], dtype=int32)

    Use ``...`` to add to a scalar ref:

    >>> ref = jax.new_ref(jax.numpy.int32(2))
    >>> ref[...] += 10
    >>> ref
    Ref(12, dtype=int32)

  .. _Ref guide: https://docs.jax.dev/en/latest/array_refs.html
  """
  ref, transforms = get_ref_and_transforms(ref, idx, "ref_addupdate")
  flat_transforms, tree = tree_util.tree_flatten(transforms)
  addupdate_p.bind(ref, x, *flat_transforms, tree=tree)

