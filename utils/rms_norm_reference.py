
def rms_norm_reference(x, weight, bias, *, eps: float = 1e-5):
  var = jnp.mean(jnp.square(x), axis=1)
  mul = lax.rsqrt(var + eps)
  return x * mul[:, None] * weight[None] + bias[None]

