
def runge_kutta_step(func, y0, f0, t0, dt):
  # Dopri5 Butcher tableaux
  alpha = jnp.array([1 / 5, 3 / 10, 4 / 5, 8 / 9, 1., 1., 0], dtype=dt.dtype)
  beta = jnp.array(
      [[1 / 5, 0, 0, 0, 0, 0, 0], [3 / 40, 9 / 40, 0, 0, 0, 0, 0],
       [44 / 45, -56 / 15, 32 / 9, 0, 0, 0, 0],
       [19372 / 6561, -25360 / 2187, 64448 / 6561, -212 / 729, 0, 0, 0],
       [9017 / 3168, -355 / 33, 46732 / 5247, 49 / 176, -5103 / 18656, 0, 0],
       [35 / 384, 0, 500 / 1113, 125 / 192, -2187 / 6784, 11 / 84, 0]],
      dtype=f0.dtype)
  c_sol = jnp.array(
      [35 / 384, 0, 500 / 1113, 125 / 192, -2187 / 6784, 11 / 84, 0],
      dtype=f0.dtype)
  c_error = jnp.array([
      35 / 384 - 1951 / 21600, 0, 500 / 1113 - 22642 / 50085, 125 / 192 -
      451 / 720, -2187 / 6784 - -12231 / 42400, 11 / 84 - 649 / 6300, -1. / 60.
  ], dtype=f0.dtype)

  def body_fun(i, k):
    ti = t0 + dt * alpha[i-1]
    yi = y0 + dt.astype(f0.dtype) * jnp.dot(beta[i-1, :], k)
    ft = func(yi, ti)
    return k.at[i, :].set(ft)

  k = jnp.zeros((7, f0.shape[0]), f0.dtype).at[0, :].set(f0)
  k = lax.fori_loop(1, 7, body_fun, k)

  y1 = dt.astype(f0.dtype) * jnp.dot(c_sol, k) + y0
  y1_error = dt.astype(f0.dtype) * jnp.dot(c_error, k)
  f1 = k[-1]
  return y1, f1, y1_error, k

