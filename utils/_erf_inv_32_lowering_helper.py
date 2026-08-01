
def _erf_inv_32_lowering_helper(x):
  k_degree = 9
  w_lt_5_constants = [
    2.81022636e-08,  3.43273939e-07, -3.5233877e-06,
    -4.39150654e-06, 0.00021858087,  -0.00125372503,
    -0.00417768164,  0.246640727,    1.50140941,
  ]
  w_gt_5_constants = [
    -0.000200214257, 0.000100950558, 0.00134934322,
    -0.00367342844,  0.00573950773,  -0.0076224613,
    0.00943887047,   1.00167406,     2.83297682,
  ]

  w = -jnp.log1p(x * -x)
  w_lt_5 = w < 5.0

  w = jnp.where(w_lt_5, w - 2.5, jnp.sqrt(w) - 3.0)

  p = jnp.where(w_lt_5, w_lt_5_constants[0], w_gt_5_constants[0])
  for i in range(1, k_degree):
    c = jnp.where(w_lt_5, w_lt_5_constants[i], w_gt_5_constants[i])
    p = c + p * w

  return jnp.where(jnp.abs(x) == 1.0, jnp.inf * x, p * x)

