from typing import Union

def selective_transform(
    optimizer: base.GradientTransformation,
    *,  # force kw-only arguments to show this is a freeze and not allow mask
    freeze_mask: Union[bool, base.ArrayTree],
) -> base.GradientTransformation:
  """Partition updates so that only un-frozen parameters are optimized.

  Example:
    >>> import jax.numpy as jnp
    >>> from optax import selective_transform
    >>> params = {'a': jnp.zeros(1), 'b': jnp.zeros(2)}
    >>> mask = {'a': True, 'b': False} # Freeze 'a', train 'b'
    >>> selective_opt = selective_transform(optax.adam(1e-3), freeze_mask=mask)

  Args:
    optimizer: The inner Optax optimizer to apply to unfrozen leaves.
    freeze_mask: A *static* mask (i.e., not dependent on runtime values or
    updated during training). It can be either:

      - a scalar bool (or 0-d JAX bool array) to freeze everything (True) or
        nothing (False)
      - a PyTree of booleans mirroring the parameter tree, marking each leaf
        to freeze (True) or train (False).

  Returns:
    A `GradientTransformation` that routes each parameter leaf through:

      - the given `optimizer` if its mask is False (“train”),
      - `set_to_zero()` if its mask is True (“freeze”).

  .. seealso::
    :func:`optax.freeze` : For simply zeroing out gradients
    according to a mask.
  """

  def label_fn(params: base.PyTree):
    del params
    return jax.tree.map(lambda m: "freeze" if m else "train", freeze_mask)

  return partition(
      {"train": optimizer, "freeze": base.set_to_zero()},
      param_labels=label_fn,
  )

