
def segment_max(data: ArrayLike,
                segment_ids: ArrayLike,
                num_segments: int | None = None,
                indices_are_sorted: bool = False,
                unique_indices: bool = False,
                bucket_size: int | None = None,
                mode: slicing.GatherScatterMode | str | None = None,
                out_sharding: NamedSharding | P | None = None) -> Array:
  """Computes the maximum within segments of an array.

  Similar to TensorFlow's `segment_max
  <https://www.tensorflow.org/api_docs/python/tf/math/segment_max>`_

  Args:
    data: an array with the values to be reduced.
    segment_ids: an array with integer dtype that indicates the segments of
      `data` (along its leading axis) to be reduced. Values can be repeated and
      need not be sorted.
    num_segments: optional, an int with nonnegative value indicating the number
      of segments. The default is set to be the minimum number of segments that
      would support all indices in ``segment_ids``, calculated as
      ``max(segment_ids) + 1``.
      Since `num_segments` determines the size of the output, a static value
      must be provided to use ``segment_max`` in a JIT-compiled function.
    indices_are_sorted: whether ``segment_ids`` is known to be sorted.
    unique_indices: whether `segment_ids` is known to be free of duplicates.
    bucket_size: size of bucket to group indices into. ``segment_max`` is
      performed on each bucket separately. Default ``None`` means no bucketing.
    mode: a :class:`jax.lax.GatherScatterMode` value describing how
      out-of-bounds indices should be handled. By default, values outside of the
      range [0, num_segments) are dropped and do not contribute to the result.

  Returns:
    An array with shape :code:`(num_segments,) + data.shape[1:]` representing the
    segment maximums.

  Examples:
    Simple 1D segment max:

    >>> data = jnp.arange(6)
    >>> segment_ids = jnp.array([0, 0, 1, 1, 2, 2])
    >>> segment_max(data, segment_ids)
    Array([1, 3, 5], dtype=int32)

    Using JIT requires static `num_segments`:

    >>> from jax import jit
    >>> jit(segment_max, static_argnums=2)(data, segment_ids, 3)
    Array([1, 3, 5], dtype=int32)
  """
  out_sharding = canonicalize_sharding(out_sharding, 'segment_max')
  if out_sharding is not None and out_sharding.spec.unreduced:
    raise NotImplementedError('unreduced for max is not yet supported.')
  return _segment_update(
      "segment_max", data, segment_ids, slicing.scatter_max, num_segments,
      indices_are_sorted, unique_indices, bucket_size, reductions.max,
      mode=mode, out_sharding=out_sharding)

