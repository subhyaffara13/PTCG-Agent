
def ones_init() -> Initializer:
  """Builds an initializer that returns a constant array full of ones.

  >>> import jax, jax.numpy as jnp
  >>> from flax.linen.initializers import ones_init
  >>> ones_initializer = ones_init()
  >>> ones_initializer(jax.random.key(42), (3, 2), jnp.float32)
  Array([[1., 1.],
         [1., 1.],
         [1., 1.]], dtype=float32)
  """
  return ones


def ones_init() -> Initializer:
  """Builds an initializer that returns a constant array full of ones.

  >>> import jax, jax.numpy as jnp
  >>> from flax.nnx import initializers
  >>> ones_initializer = initializers.ones_init()
  >>> ones_initializer(jax.random.key(42), (3, 2), jnp.float32)
  Array([[1., 1.],
         [1., 1.],
         [1., 1.]], dtype=float32)
  """
  return ones

