
def FanInSum():
  """Layer construction function for a fan-in sum layer."""
  init_fun = lambda rng, input_shape: (input_shape[0], ())
  apply_fun = lambda params, inputs, **kwargs: sum(inputs)
  return init_fun, apply_fun

