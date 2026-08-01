
def per_example_global_norm_clip(
    grads: base.ArrayTree, l2_norm_clip: jax.typing.ArrayLike  # float
) -> tuple[base.ArrayTree, jax.Array]:
  """Applies gradient clipping per-example using their global norm.

  Args:
    grads: flattened update; the function expects each array in this list to
      have a batch dimension on the 0th axis.
    l2_norm_clip: maximum L2 norm of the per-example gradients.

  Returns:
    A tuple containing sum of the clipped per-example grads, and the number of
    per-example grads that were clipped.

  Example:
    >>> import optax
    >>> import jax.numpy as jnp
    >>> grads = [jnp.array([[0, 0, 0], [0, 3, 4], [4, 0, 3], [3, 4, 0]])]
    >>> optax.per_example_global_norm_clip(grads, jnp.inf)
    ([Array([7., 7., 7.], dtype=float32)], Array(0, dtype=int32))
    >>> optax.per_example_global_norm_clip(grads, 0.0)
    ([Array([0., 0., 0.], dtype=float32)], Array(3, dtype=int32))
    >>> optax.per_example_global_norm_clip(grads, 1.25)
    ([Array([1.75, 1.75, 1.75], dtype=float32)], Array(3, dtype=int32))

  References:
    Abadi et al., `Deep Learning with Differential Privacy
    <https://arxiv.org/abs/1607.00133>`_, 2016

  .. seealso::
    :func:`optax.contrib.differentially_private_aggregate` for more realistic
    example usages.
  """

  if not _check_arrays_have_batch_dim(grads):
    raise ValueError(
        "Unlike other transforms, `per_example_global_norm_clip` expects"
        " `grads` to have a batch dimension in the 0th axis."
    )

  global_grad_norms = jax.vmap(optax.tree.norm)(grads)
  multipliers = jnp.nan_to_num(
      jnp.minimum(l2_norm_clip / global_grad_norms, 1.0), nan=1.0
  )
  num_clipped = jnp.sum(multipliers < 1.0)
  clipped_sum = jax.tree.map(
      lambda g: jnp.tensordot(multipliers, g, axes=1), grads
  )
  return clipped_sum, num_clipped

