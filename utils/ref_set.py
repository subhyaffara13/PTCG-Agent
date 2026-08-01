
def ref_set(
    ref: core.Ref | TransformedRef,
    idx: Indexer | tuple[Indexer, ...] | None,
    value: ArrayLike | HijaxType,
) -> None:
  """Set a value in an Ref in-place.

  This is equivalent to ``ref[idx] = value`` for a NumPy-style indexer
  ``idx``. For more on mutable array refs, refer to the `Ref guide`_.

  Args:
    ref: a :class:`jax.ref.Ref` object. On return, the buffer will be
      mutated by this operation.
    idx: a NumPy-style indexer
    value: a :class:`jax.Array` object (note, not a :class:`jax.ref.Ref`)
      containing the values to set in the array.

  Returns:
    None

  Examples:
    >>> import jax
    >>> ref = jax.new_ref(jax.numpy.zeros(5))
    >>> jax.ref.set(ref, 1, 10.0)
    >>> ref
    Ref([ 0., 10.,  0.,  0.,  0.], dtype=float32)

    Equivalent operation via indexing syntax:

    >>> ref = jax.new_ref(jax.numpy.zeros(5))
    >>> ref[1] = 10.0
    >>> ref
    Ref([ 0., 10.,  0.,  0.,  0.], dtype=float32)

    Use ``...`` to set the value of a scalar ref:

    >>> ref = jax.new_ref(jax.numpy.int32(0))
    >>> ref[...] = 4
    >>> ref
    Ref(4, dtype=int32)

  .. _Ref guide: https://docs.jax.dev/en/latest/array_refs.html
  """
  ref_swap(ref, idx, value, _function_name="ref_set")

