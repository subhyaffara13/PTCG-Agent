
def shape_dependent(make_layer):
  """Combinator to delay layer constructor pair until input shapes are known.

  Args:
    make_layer: a one-argument function that takes an input shape as an argument
      (a tuple of positive integers) and returns an (init_fun, apply_fun) pair.

  Returns:
    A new layer, meaning an (init_fun, apply_fun) pair, representing the same
    layer as returned by `make_layer` but with its construction delayed until
    input shapes are known.
  """
  def init_fun(rng, input_shape):
    return make_layer(input_shape)[0](rng, input_shape)
  def apply_fun(params, inputs, **kwargs):
    return make_layer(inputs.shape)[1](params, inputs, **kwargs)
  return init_fun, apply_fun

