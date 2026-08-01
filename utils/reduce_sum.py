
def reduce_sum(values, index, name="segmented_reduce_sum"):
    """
    Sums a tensor over its segments.

    Outputs 0 for empty segments.

    This operations computes the sum over segments, with support for:

        - Batching using the first dimensions [B1, B2, ..., Bn]. Each element in a batch can have different indices.
        - Vectorization using the last dimension [V1, V2, ...]. If they are present, the output will be a sum of
          vectors rather than scalars. Only the middle dimensions [I1, ..., Ik] are reduced by the operation.

    Args:
        values (`torch.Tensor` of shape [B1, B2, ..., Bn, I1, .., Ik, V1, V2, ..]):
            Tensor containing the values of which the sum must be taken segment-wise.
        index (`IndexMap`, indices are of shape [B1, B2, ..., Bn, I1, .., Ik].):
            Index defining the segments.
        name (`str`, *optional*, defaults to 'segmented_reduce_sum'):
            Name for the operation. Currently not used

    Returns:
        output_values (`torch.Tensor`of shape [B1, B2, ..., Bn, num_segments, V1, V2, ..]): Tensor containing the
        output values. output_index (`IndexMap`): IndexMap with shape [B1, B2, ..., Bn, num_segments]. .
    """
    return _segment_reduce(values, index, "sum", name)


def reduce_sum(operand: ArrayLike, axes: Sequence[int], *,
               out_sharding=None) -> Array:
  """Compute the sum of elements over one or more array axes.

  Args:
    operand: array over which to sum. Must have numerical dtype.
    axes: sequence of zero or more unique integers specifying the axes over
      which to sum. Each entry must satisfy ``0 <= axis < operand.ndim``.

  Returns:
    An array of the same dtype as ``operand``, with shape corresponding
    to the dimensions of ``operand.shape`` with ``axes`` removed.

  Notes:
    Unlike :func:`jax.numpy.sum`, :func:`jax.lax.reduce_sum` does not upcast
    narrow-width types for accumulation, so sums of 8-bit or 16-bit types
    may be subject to rounding errors.

  See also:
    - :func:`jax.numpy.sum`: more flexible NumPy-style summation API, built
      around :func:`jax.lax.reduce_sum`.
    - Other low-level :mod:`jax.lax` reduction operators:
      :func:`jax.lax.reduce_prod`, :func:`jax.lax.reduce_max`, :func:`jax.lax.reduce_min`,
      :func:`jax.lax.reduce_and`, :func:`jax.lax.reduce_or`, :func:`jax.lax.reduce_xor`.
  """
  out_sharding = canonicalize_sharding(out_sharding, 'reduce_sum')
  return reduce_sum_p.bind(operand, axes=tuple(axes), out_sharding=out_sharding)

