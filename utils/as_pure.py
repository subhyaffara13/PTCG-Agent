
def as_pure(tree: A) -> A:
  """Returns a new tree with all ``Variable`` objects replaced with inner values.

  This can be used to remove Variable metadata when its is not needed for tasks like
  serialization or exporting.

  Example::

    >>> from flax import nnx
    >>> import jax
    >>> import jax.numpy as jnp
    ...
    >>> model = nnx.Linear(2, 3, rngs=nnx.Rngs(0))
    >>> graphdef, state = nnx.split(model)
    >>> jax.tree.map(jnp.shape, state)
    State({
      'bias': Param(
        value=(3,)
      ),
      'kernel': Param(
        value=(2, 3)
      )
    })
    >>> pure_state = nnx.as_pure(state)
    >>> jax.tree.map(jnp.shape, pure_state)
    State({
      'bias': (3,),
      'kernel': (2, 3)
    })

  Args:
    tree: A pytree potentially containing ``Variable`` objects.
  Returns:
    A new pytree with all ``Variable`` objects replaced with their
    inner values.
  """

  def _pure_fn(x):
    if isinstance(x, Variable):
      return as_pure(x.get_raw_value())
    elif variablelib.is_array_ref(x):
      return x[...]
    return x

  return jax.tree.map(
    _pure_fn,
    tree,
    is_leaf=lambda x: isinstance(x, Variable),
  )

