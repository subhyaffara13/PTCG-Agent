
def ensure_compile_time_eval():
  """Context manager to ensure evaluation at trace/compile time (or error).

  Some JAX APIs like :func:`jax.jit` and :func:`jax.lax.scan` involve staging,
  i.e., delaying the evaluation of numerical expressions (like :mod:`jax.numpy`
  function applications) so that instead of performing those computations
  eagerly while evaluating the corresponding Python expressions, their
  computation is carried out separately, e.g. after optimized compilation. But
  this delay can be undesirable. For example, numerical values might be needed
  to evaluate Python control flow and so their evaluation cannot be delayed. As
  another example, it may be beneficial to ensure compile time evaluation (or
  "constant folding") for performance reasons.

  This context manager ensures that JAX computations are evaluated eagerly. If
  eager evaluation is not possible, a ``ConcretizationTypeError`` is raised.

  Here's a contrived example::

    import jax
    import jax.numpy as jnp

    @jax.jit
    def f(x):
      with jax.ensure_compile_time_eval():
        y = jnp.sin(3.0)
        z = jnp.sin(y)
        z_positive = z > 0
      if z_positive:  # z_positive is usable in Python control flow
        return jnp.sin(x)
      else:
        return jnp.cos(x)

  Here's a real-world example from https://github.com/jax-ml/jax/issues/3974::

    import jax
    import jax.numpy as jnp
    from jax import random

    @jax.jit
    def jax_fn(x):
      with jax.ensure_compile_time_eval():
        y = random.randint(random.key(0), (1000,1000), 0, 100)
      y2 = y @ y
      x2 = jnp.sum(y2) * x
      return x2

  A similar behavior can often be achieved simply by 'hoisting' the constant
  expression out of the corresponding staging API::

    y = random.randint(random.key(0), (1000,1000), 0, 100)

    @jax.jit
    def jax_fn(x):
      y2 = y @ y
      x2 = jnp.sum(y2)*x
      return x2

  But in some cases it can be more convenient to use this context manager.
  """
  with config.eager_constant_folding(True):
    yield

