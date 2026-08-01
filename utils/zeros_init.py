
def zeros_init() -> Initializer:
  """Builds an initializer that returns a constant array full of zeros.

  >>> import jax, jax.numpy as jnp
  >>> from flax.linen.initializers import zeros_init
  >>> zeros_initializer = zeros_init()
  >>> zeros_initializer(jax.random.key(42), (2, 3), jnp.float32)
  Array([[0., 0., 0.],
         [0., 0., 0.]], dtype=float32)
  """
  return zeros


def zeros_init() -> Initializer:
  """Builds an initializer that returns a constant array full of zeros.

  >>> import jax, jax.numpy as jnp
  >>> from flax.nnx import initializers
  >>> zeros_initializer = initializers.zeros_init()
  >>> zeros_initializer(jax.random.key(42), (2, 3), jnp.float32)
  Array([[0., 0., 0.],
         [0., 0., 0.]], dtype=float32)
  """
  return zeros

