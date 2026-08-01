
def make_user_context(default_value=None):
  """Creates a `jax.jit` cache sensitive context.

  If the value of the context changes, JAX's tracing, lowering and compilation
  cache won't get a hit and the jitted function will be re-traced, re-lowered
  and re-compiled.

  Adding new user contexts is not thread-safe. Do not call make_user_context
  concurrently with other JAX APIs. However, using a user context once it has
  been constructed is thread-safe.

  Example:

  ```
  @jax.jit
  def f(x):
    return x * 2

  my_context = jax.make_user_context(default_value=None)
  with my_context(1):
    f(1.)
  with my_context(2):
    f(1.)  # tracing cache miss
  ```
  """
  return UserConfig(default_value)

