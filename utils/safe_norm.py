from typing import Optional, Union

def safe_norm(
    x: jax.typing.ArrayLike,
    min_norm: jax.typing.ArrayLike,
    ord: Optional[Union[int, float, str]] = None,  # pylint: disable=redefined-builtin
    axis: Union[None, tuple[int, ...], int] = None,
    keepdims: bool = False,
) -> jax.Array:
  """Returns jnp.maximum(jnp.linalg.norm(x), min_norm) with correct gradients.

  The gradients of `jnp.maximum(jnp.linalg.norm(x), min_norm)` at 0.0 is `NaN`,
  because jax will evaluate both branches of the `jnp.maximum`. This function
  will instead return the correct gradient of 0.0 also in such setting.

  Args:
    x: jax array.
    min_norm: lower bound for the returned norm.
    ord: {non-zero int, inf, -inf, 'fro', 'nuc'}, optional. Order of the norm.
      inf means numpy's inf object. The default is None.
    axis: {None, int, 2-tuple of ints}, optional. If axis is an integer, it
      specifies the axis of x along which to compute the vector norms. If axis
      is a 2-tuple, it specifies the axes that hold 2-D matrices, and the matrix
      norms of these matrices are computed. If axis is None then either a vector
      norm (when x is 1-D) or a matrix norm (when x is 2-D) is returned. The
      default is None.
    keepdims: bool, optional. If this is set to True, the axes which are normed
      over are left in the result as dimensions with size one. With this option
      the result will broadcast correctly against the original x.

  Returns:
    The safe norm of the input vector, accounting for correct gradient.
  """
  norm = jnp.linalg.norm(x, ord=ord, axis=axis, keepdims=True)
  x = jnp.where(norm <= min_norm, jnp.ones_like(x), x)
  norm = jnp.squeeze(norm, axis=axis) if not keepdims else norm
  masked_norm = jnp.linalg.norm(x, ord=ord, axis=axis, keepdims=keepdims)
  return jnp.where(norm <= min_norm, min_norm, masked_norm)

