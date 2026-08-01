
def _bessel_jn_scan_body_fun(carry, k):
  f0, f1, bs, z = carry
  f = 2.0 * (k + 1.0) * f1 / z - f0

  def true_fn_update_bs(u):
    bs, f = u
    return bs + 2.0 * f

  def false_fn_update_bs(u):
    bs, _ = u
    return bs

  bs = lax.cond(jnp.mod(k, 2) == 0, true_fn_update_bs,
                false_fn_update_bs, operand=(bs, f))

  f0 = f1
  f1 = f
  return (f0, f1, bs, z), f

