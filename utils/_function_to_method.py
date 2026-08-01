
def _function_to_method(random_f):
  @functools.wraps(random_f)
  def rngs_random_method(self: Rngs | RngStream, *args, **kwargs) -> jax.Array:
    return random_f(self(), *args, **kwargs)

  return rngs_random_method

