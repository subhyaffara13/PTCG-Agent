
def interp_fit_dopri(y0, y1, k, dt):
  # Fit a polynomial to the results of a Runge-Kutta step.
  dps_c_mid = jnp.array([
      6025192743 / 30085553152 / 2, 0, 51252292925 / 65400821598 / 2,
      -2691868925 / 45128329728 / 2, 187940372067 / 1594534317056 / 2,
      -1776094331 / 19743644256 / 2, 11237099 / 235043384 / 2], dtype=y0.dtype)
  y_mid = y0 + dt.astype(y0.dtype) * jnp.dot(dps_c_mid, k)
  return jnp.asarray(fit_4th_order_polynomial(y0, y1, y_mid, k[0], k[-1], dt))

