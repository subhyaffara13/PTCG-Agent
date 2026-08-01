
def Dense(out_dim, W_init=glorot_normal(), b_init=normal()):
  """Layer constructor function for a dense (fully-connected) layer."""
  def init_fun(rng, input_shape):
    output_shape = input_shape[:-1] + (out_dim,)
    k1, k2 = random.split(rng)
    W, b = W_init(k1, (input_shape[-1], out_dim)), b_init(k2, (out_dim,))
    return output_shape, (W, b)
  def apply_fun(params, inputs, **kwargs):
    W, b = params
    return jnp.dot(inputs, W) + b
  return init_fun, apply_fun


def dense(
  scope,
  inputs,
  features,
  bias=True,
  dtype=jnp.float32,
  precision=None,
  kernel_init=default_kernel_init,
  bias_init=initializers.zeros_init(),
):
  """Applies a linear transformation to the inputs along the last dimension.

  Args:
    inputs: The nd-array to be transformed.
    features: the number of output features.
    bias: whether to add a bias to the output (default: True).
    dtype: the dtype of the computation (default: float32).
    precision: numerical precision of the computation see `jax.lax.Precision`
      for details.
    kernel_init: initializer function for the weight matrix.
    bias_init: initializer function for the bias.
  Returns:
    The transformed input.
  """
  inputs = jnp.asarray(inputs, dtype)
  kernel = scope.param('kernel', kernel_init, (inputs.shape[-1], features))
  kernel = jnp.asarray(kernel, dtype)
  y = lax.dot_general(
    inputs,
    kernel,
    (((inputs.ndim - 1,), (0,)), ((), ())),
    precision=precision,
  )
  if bias:
    bias = scope.param('bias', bias_init, (features,))
    bias = jnp.asarray(bias, dtype)
    y += jnp.reshape(bias, (1,) * (y.ndim - 1) + (-1,))
  return y

