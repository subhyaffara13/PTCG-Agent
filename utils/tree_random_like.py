from typing import Callable, Optional, Union

def tree_random_like(
    rng_key: base.PRNGKey,
    target_tree: base.ArrayTree,
    sampler: Union[
        Callable[[base.PRNGKey, base.Shape, jax.typing.DTypeLike],
                 jax.typing.ArrayLike],
        Callable[[base.PRNGKey, base.Shape, jax.typing.DTypeLike,
                  jax.sharding.Sharding],
                 jax.typing.ArrayLike]] = jax.random.normal,
    dtype: Optional[jax.typing.DTypeLike] = None,
) -> base.ArrayTree:
  """Create tree with random entries of the same shape as target tree.

  Args:
    rng_key: the key for the random number generator.
    target_tree: the tree whose structure to match. Leaves must be arrays.
    sampler: the noise sampling function, by default ``jax.random.normal``.
    dtype: the desired dtype for the random numbers, passed to ``sampler``. If
      None, the dtype of the target tree is used if possible.

  Returns:
    a random tree with the same structure as ``target_tree``, whose leaves have
    distribution ``sampler``.

  .. warning::
    The possible dtypes may be limited by the sampler, for example
    ``jax.random.rademacher`` only supports integer dtypes and will raise an
    error if the dtype of the target tree is not an integer or if the dtype
    is not of integer type.

  .. versionadded:: 0.2.1
  """
  keys_tree = tree_split_key_like(rng_key, target_tree)
  sampler_ = sampler
  if "out_sharding" not in inspect.signature(sampler).parameters:
    sampler_ = lambda key, shape, dtype, *, out_sharding: sampler(  # pylint: disable=unnecessary-lambda
        key, shape, dtype)  # pytype: disable=wrong-arg-count
  return jax.tree.map(
      # pytype: disable=wrong-keyword-args
      lambda leaf, key: sampler_(key, leaf.shape, dtype or leaf.dtype,
                                 out_sharding=jax.typeof(leaf).sharding),
      # pytype: enable=wrong-keyword-args
      target_tree,
      keys_tree,
  )

