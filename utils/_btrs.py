
def _btrs(key, count, prob, shape, dtype, max_iters):
  # transforman-rejection algorithm
  # https://www.tandfonline.com/doi/abs/10.1080/00949659308811496
  stddev = jnp.sqrt(count * prob * (1 - prob))
  b = 1.15 + 2.53 * stddev
  a = -0.0873 + 0.0248 * b + 0.01 * prob
  c = count * prob + 0.5
  v_r = 0.92 - 4.2 / b
  r = prob / (1 - prob)
  alpha = (2.83 + 5.1 / b) * stddev
  m = jnp.floor((count + 1) * prob)

  def body_fn(carry):
    i, k_out, accepted, key = carry
    key, subkey_0, subkey_1 = split(key, 3)
    u = uniform(subkey_0, shape, prob.dtype)
    v = uniform(subkey_1, shape, prob.dtype)
    u = u - 0.5
    us = 0.5 - jnp.abs(u)
    accept1 = (us >= 0.07) & (v <= v_r)
    k = jnp.floor((2 * a / us + b) * u + c)
    reject = (k < 0) | (k > count)
    v = jnp.log(v * alpha / (a / (us * us) + b))
    ub = (
      (m + 0.5) * jnp.log((m + 1) / (r * (count - m + 1)))
      + (count + 1) * jnp.log((count - m + 1) / (count - k + 1))
      + (k + 0.5) * jnp.log(r * (count - k + 1) / (k + 1))
      + _stirling_approx_tail(m)
      + _stirling_approx_tail(count - m)
      - _stirling_approx_tail(k)
      - _stirling_approx_tail(count - k)
    )
    accept2 = v <= ub
    accept = accept1 | (~reject & accept2)
    k_out = lax.select(accept, k, k_out)
    accepted |= accept
    return i + 1, k_out, accepted, key

  def cond_fn(carry):
    i, accepted = carry[0], carry[2]
    return (~accepted).any() & (i < max_iters)

  k_init = lax.full_like(prob, -1, prob.dtype, shape)
  carry = (0, k_init, jnp.full(shape, False, bool), key)
  return lax_control_flow.while_loop(cond_fn, body_fn, carry)[1].astype(dtype)

