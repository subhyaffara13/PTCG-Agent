
def _odeint_rev(func, rtol, atol, mxstep, hmax, res, g):
  ys, ts, args = res

  def aug_dynamics(augmented_state, t, *args):
    """Original system augmented with vjp_y, vjp_t and vjp_args."""
    y, y_bar, *_ = augmented_state
    # `t` here is negatice time, so we need to negate again to get back to
    # normal time. See the `odeint` invocation in `scan_fun` below.
    y_dot, vjpfun = jax.vjp(func, y, -t, *args)
    return (-y_dot, *vjpfun(y_bar))

  y_bar = g[-1]
  ts_bar = []
  t0_bar = 0.

  def scan_fun(carry, i):
    y_bar, t0_bar, args_bar = carry
    # Compute effect of moving measurement time
    # `t_bar` should not be complex as it represents time
    t_bar = jnp.dot(func(ys[i], ts[i], *args), g[i]).real
    t0_bar = t0_bar - t_bar
    # Run augmented system backwards to previous observation
    _, y_bar, t0_bar, args_bar = odeint(
        aug_dynamics, (ys[i], y_bar, t0_bar, args_bar),
        jnp.array([-ts[i], -ts[i - 1]]),
        *args, rtol=rtol, atol=atol, mxstep=mxstep, hmax=hmax)
    y_bar, t0_bar, args_bar = tree_map(op.itemgetter(1), (y_bar, t0_bar, args_bar))
    # Add gradient from current output
    y_bar = y_bar + g[i - 1]
    return (y_bar, t0_bar, args_bar), t_bar

  init_carry = (g[-1], 0., tree_map(jnp.zeros_like, args))
  (y_bar, t0_bar, args_bar), rev_ts_bar = lax.scan(
      scan_fun, init_carry, jnp.arange(len(ts) - 1, 0, -1))
  ts_bar = jnp.concatenate([jnp.array([t0_bar]), rev_ts_bar[::-1]])
  return (y_bar, ts_bar, *args_bar)

