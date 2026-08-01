
def logmeanexp(
    x: ArrayLike,
    axis: Axis = None,
    where: ArrayLike | None = None,
    keepdims: bool = False,
) -> Array:
  r"""Log mean exp.

  Computes the function:

  .. math::
    \text{logmeanexp}(x) = \log \frac{1}{n} \sum_{i=1}^n \exp x_i = \text{logsumexp}(x) - \log n

  Args:
    x: Input array.
    axis: Axis or axes along which to reduce.
    where: Elements to include in the reduction. Optional.
    keepdims: Preserve the dimensions of the input.
  Returns:
    An array.
  See also:
    :func:`jax.nn.logsumexp`
  """
  lse = _logsumexp(x, axis=axis, where=where, keepdims=keepdims)
  count = _count(x, axis=axis, where=where, keepdims=keepdims, dtype=lse.dtype)
  return lse - jnp.log(count)

