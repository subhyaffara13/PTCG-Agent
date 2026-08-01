
def _default_einshape_kernel(equation: str, x: jax_typing.Array, **sizes: int):
  return _einshape(equation, x, **sizes)

