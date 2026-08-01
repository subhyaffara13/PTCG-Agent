
def FanOut(num):
  """Layer construction function for a fan-out layer."""
  init_fun = lambda rng, input_shape: ([input_shape] * num, ())
  apply_fun = lambda params, inputs, **kwargs: [inputs] * num
  return init_fun, apply_fun

