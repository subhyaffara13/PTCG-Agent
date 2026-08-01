
def reduce_max(values, index, name="segmented_reduce_max"):
    """
    Computes the maximum over segments.

    This operation computes the maximum over segments, with support for:

        - Batching using the first dimensions [B1, B2, ..., Bn]. Each element in a batch can have different indices.
        - Vectorization using the last dimension [V1, V2, ...]. If they are present, the output will be an element-wise
          maximum of vectors rather than scalars.

    Only the middle dimensions [I1, ..., Ik] are reduced by the operation.

    Args:
        values (`torch.Tensor` of shape [B1, B2, ..., Bn, I1, .., Ik, V1, V2, ..]):
            Tensor containing the values of which the max must be taken segment-wise.
        index (`IndexMap`, indices are of shape [B1, B2, ..., Bn, I1, .., Ik].):
            Index defining the segments.
        name (`str`, *optional*, defaults to 'segmented_reduce_sum'):
            Name for the operation. Currently not used

    Returns:
        output_values (`torch.Tensor`of shape [B1, B2, ..., Bn, num_segments, V1, V2, ..]): Tensor containing the
        output values. output_index (`IndexMap`): IndexMap with shape [B1, B2, ..., Bn, num_segments].
    """
    return _segment_reduce(values, index, "amax", name)


def reduce_max(x, dim=None, keepdim=False):
    if dim is not None:
        return (
            reduce_amax(x, axis=dim, keepdims=keepdim),
            reduce_argmax(x, axis=dim, keepdims=keepdim),
        )

    return reduce_amax(x, axis=None, keepdims=keepdim)


def reduce_max(operand: ArrayLike, axes: Sequence[int]) -> Array:
  """Compute the maximum of elements over one or more array axes.

  Args:
    operand: array over which to compute maximum.
    axes: sequence of zero or more unique integers specifying the axes over
      which to reduce. Each entry must satisfy ``0 <= axis < operand.ndim``.

  Returns:
    An array of the same dtype as ``operand``, with shape corresponding
    to the dimensions of ``operand.shape`` with ``axes`` removed.

  See also:
    - :func:`jax.numpy.max`: more flexible NumPy-style max-reduction API, built
      around :func:`jax.lax.reduce_max`.
    - Other low-level :mod:`jax.lax` reduction operators:
      :func:`jax.lax.reduce_sum`, :func:`jax.lax.reduce_prod`, :func:`jax.lax.reduce_min`,
      :func:`jax.lax.reduce_and`, :func:`jax.lax.reduce_or`, :func:`jax.lax.reduce_xor`.
  """
  return reduce_max_p.bind(operand, axes=tuple(axes))

