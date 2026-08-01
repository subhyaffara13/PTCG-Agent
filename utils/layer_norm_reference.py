
def layer_norm_reference(x, weight, bias, *, eps: float = 1e-5):
  mean = jnp.mean(x, axis=1)
  mean2 = jnp.mean(jnp.square(x), axis=1)
  var = jnp.maximum(0., mean2 - jnp.square(mean))
  y = x - mean[:, None]
  mul = lax.rsqrt(var + eps)
  return y * mul[:, None] * weight[None] + bias[None]

