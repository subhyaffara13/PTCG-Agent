
def broadcast_like(arr: ArrayLike, like_arr: ArrayLike) -> Array:
  """Broadcasts an array to match the shape and sharding of another array.

  Args:
    arr: an array to be broadcasted.
    like_arr: an array whose shape and sharding should be matched.

  Returns:
    An array containing the broadcasted values of ``arr``.

  See also:
    - :func:`jax.lax.broadcast`: simpler interface to add new leading dimensions.
    - :func:`jax.lax.broadcast_in_dim`: general broadcasting at any dimension in the array.
    - :func:`jax.numpy.broadcast_to`: NumPy-style API for general broadcasting.

  Examples:
    >>> import jax.numpy as jnp
    >>> from jax import lax
    >>> arr = jnp.array([1, 2, 3])
    >>> like_arr = jnp.zeros((2, 3))
    >>> lax.broadcast_like(arr, like_arr)
    Array([[1, 2, 3],
           [1, 2, 3]], dtype=int32)
  """
  like_aval = core.typeof(like_arr)
  return broadcast_to(arr, shape=like_aval.shape, sharding=like_aval.sharding)

