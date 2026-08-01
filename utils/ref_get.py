
def ref_get(
    ref: core.Ref | TransformedRef,
    idx: Indexer | tuple[Indexer, ...] | None = None
) -> Array | HijaxType:
  """Read a value from an Ref.

  This is equivalent to ``ref[idx]`` for a NumPy-style indexer ``idx``.
  For more on mutable array refs, refer to the `Ref guide`_.

  Args:
    ref: a :class:`jax.ref.Ref` object.
    idx: a NumPy-style indexer

  Returns:
    A :class:`jax.Array` object (note, not a :class:`jax.ref.Ref`) containing
    the indexed elements of the mutable reference.

  Examples:
    >>> import jax
    >>> ref = jax.new_ref(jax.numpy.arange(5))
    >>> jax.ref.get(ref, slice(1, 3))
    Array([1, 2], dtype=int32)

    Equivalent operation via indexing syntax:

    >>> ref[1:3]
    Array([1, 2], dtype=int32)

    Use ``...`` to extract the full buffer:

    >>> ref[...]
    Array([0, 1, 2, 3, 4], dtype=int32)

  .. _Ref guide: https://docs.jax.dev/en/latest/array_refs.html
  """
  if isinstance(ref, TransformedRef) and ref.multiref:
    raise NotImplementedError(
        "ref_get with multi-ref TransformedRef is not supported."
    )
  ref, transforms = get_ref_and_transforms(ref, idx, "ref_get")
  flat_transforms, tree = tree_util.tree_flatten(transforms)
  return get_p.bind(ref, *flat_transforms, tree=tree)

