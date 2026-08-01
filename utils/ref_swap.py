
def ref_swap(
    ref: core.Ref | TransformedRef,
    idx: Indexer | tuple[Indexer, ...] | None,
    value: ArrayLike | HijaxType,
    _function_name: str = "ref_swap",
) -> Array | HijaxType:
  """Update an array value inplace while returning the previous value.

  This is equivalent to ``ref[idx], prev = value, ref[idx]`` while returning
  ``prev``, for a NumPy-style indexer ``idx``.
  For more on mutable array refs, refer to the `Ref guide`_.

  Args:
    ref: a :class:`jax.ref.Ref` object. On return, the buffer will be
      mutated by this operation.
    idx: a NumPy-style indexer
    value: a :class:`jax.Array` object (note, not a :class:`jax.ref.Ref`)
      containing the values to set in the array.

  Returns:
    A :class:`jax.Array` containing the previous value at `idx`.

  Examples:
    >>> import jax
    >>> ref = jax.new_ref(jax.numpy.arange(5))
    >>> jax.ref.swap(ref, 3, 10)
    Array(3, dtype=int32)
    >>> ref
    Ref([ 0,  1,  2, 10,  4], dtype=int32)

    Equivalent operation via indexing syntax:

    >>> ref = jax.new_ref(jax.numpy.arange(5))
    >>> ref[3], prev = 10, ref[3]
    >>> prev
    Array(3, dtype=int32)
    >>> ref
    Ref([ 0,  1,  2, 10,  4], dtype=int32)

    Use ``...`` to swap the value of a scalar ref:

    >>> ref = jax.new_ref(jax.numpy.int32(5))
    >>> jax.ref.swap(ref, ..., 10)
    Array(5, dtype=int32)
    >>> ref
    Ref(10, dtype=int32)

  .. _Ref guide: https://docs.jax.dev/en/latest/array_refs.html
  """
  if isinstance(ref, TransformedRef) and ref.multiref:
    raise NotImplementedError(
        "ref_swap with multi-ref TransformedRef is not supported."
    )
  if hasattr(ref, 'dtype'):
    value = _maybe_implicit_cast(ref.dtype, value)
  ref, transforms = get_ref_and_transforms(ref, idx, _function_name)
  flat_transforms, tree = tree_util.tree_flatten(transforms)
  return swap_p.bind(ref, value, *flat_transforms, tree=tree)

