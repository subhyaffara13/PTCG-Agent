
def _odeint(func, rtol, atol, mxstep, hmax, y0, ts, *args):
  func_ = lambda y, t: func(y, t, *args)

  def scan_fun(carry, target_t):

    def cond_fun(state):
      i, _, _, t, dt, _, _ = state
      return (t < target_t) & (i < mxstep) & (dt > 0)

    def body_fun(state):
      i, y, f, t, dt, last_t, interp_coeff = state
      next_y, next_f, next_y_error, k = runge_kutta_step(func_, y, f, t, dt)
      next_t = t + dt
      error_ratio = mean_error_ratio(next_y_error, rtol, atol, y, next_y)
      new_interp_coeff = interp_fit_dopri(y, next_y, k, dt)
      dt = jnp.clip(optimal_step_size(dt, error_ratio), min=0., max=hmax)

      new = [i + 1, next_y, next_f, next_t, dt,      t, new_interp_coeff]
      old = [i + 1,      y,      f,      t, dt, last_t,     interp_coeff]
      return map(partial(jnp.where, error_ratio <= 1.), new, old)

    _, *carry = lax.while_loop(cond_fun, body_fun, [0] + carry)
    _, _, t, _, last_t, interp_coeff = carry
    relative_output_time = (target_t - last_t) / (t - last_t)
    y_target = jnp.polyval(interp_coeff, relative_output_time.astype(interp_coeff.dtype))
    return carry, y_target

  f0 = func_(y0, ts[0])
  dt = jnp.clip(initial_step_size(func_, ts[0], y0, 4, rtol, atol, f0), min=0., max=hmax)
  interp_coeff = jnp.array([y0] * 5)
  init_carry = [y0, f0, ts[0], dt, ts[0], interp_coeff]
  _, ys = lax.scan(scan_fun, init_carry, ts[1:])
  return jnp.concatenate((y0[None], ys))

