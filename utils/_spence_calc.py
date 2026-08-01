
def _spence_calc(x: Array) -> Array:
  x2_bool = x > 2.0
  x = jnp.piecewise(x, [x2_bool],
                    [lambda x: 1.0 / x, lambda x: x])

  x1_5_bool = x > 1.5
  x_5_bool = x < 0.5
  x2_bool = x2_bool | x1_5_bool

  w = jnp.piecewise(x,
                    [x1_5_bool, x_5_bool],
                    [lambda x: 1.0 / x - 1.0,
                      lambda x: -x,
                      lambda x: x - 1.0])

  y = _spence_poly(w)
  y_flag_one = np.pi ** 2 / 6.0 - jnp.log(x) * jnp.log(1.0 - x) - y
  y = jnp.where(x_5_bool, y_flag_one, y)
  y_flag_two = -0.5 * jnp.log(x) ** 2 - y
  return jnp.where(x2_bool, y_flag_two, y)

