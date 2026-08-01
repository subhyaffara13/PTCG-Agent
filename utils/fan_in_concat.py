
def FanInConcat(axis=-1):
  """Layer construction function for a fan-in concatenation layer."""
  def init_fun(rng, input_shape):
    ax = axis % len(input_shape[0])
    concat_size = sum(shape[ax] for shape in input_shape)
    out_shape = input_shape[0][:ax] + (concat_size,) + input_shape[0][ax+1:]
    return out_shape, ()
  def apply_fun(params, inputs, **kwargs):
    return jnp.concatenate(inputs, axis)
  return init_fun, apply_fun

