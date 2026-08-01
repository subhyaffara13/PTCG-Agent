
def line_search(f, xk, pk, old_fval=None, old_old_fval=None, gfk=None, c1=1e-4,
                c2=0.9, maxiter=20):
  """Inexact line search that satisfies strong Wolfe conditions.

  Algorithm 3.5 from Wright and Nocedal, 'Numerical Optimization', 1999, pg. 59-61

  Args:
    fun: function of the form f(x) where x is a flat ndarray and returns a real
      scalar. The function should be composed of operations with vjp defined.
    x0: initial guess.
    pk: direction to search in. Assumes the direction is a descent direction.
    old_fval, gfk: initial value of value_and_gradient as position.
    old_old_fval: unused argument, only for scipy API compliance.
    maxiter: maximum number of iterations to search
    c1, c2: Wolfe criteria constant, see ref.

  Returns: LineSearchResults
  """
  xk, pk = promote_dtypes_inexact(xk, pk)
  def restricted_func_and_grad(t):
    t = jnp.array(t, dtype=pk.dtype)
    phi, g = api.value_and_grad(f)(xk + t * pk)
    dphi = jnp.real(_dot(g, pk))
    return phi, dphi, g

  if old_fval is None or gfk is None:
    phi_0, dphi_0, gfk = restricted_func_and_grad(0)
  else:
    phi_0 = old_fval
    dphi_0 = jnp.real(_dot(gfk, pk))
  if old_old_fval is not None:
    candidate_start_value = 1.01 * 2 * (phi_0 - old_old_fval) / dphi_0
    start_value = jnp.where(candidate_start_value > 1, 1.0, candidate_start_value)
  else:
    start_value = 1

  def wolfe_one(a_i, phi_i) -> Array:
    # actually negation of W1
    return phi_i > phi_0 + c1 * a_i * dphi_0

  def wolfe_two(dphi_i) -> Array:
    return jnp.abs(dphi_i) <= -c2 * dphi_0

  state = _LineSearchState(
      done=jnp.array(False, dtype=bool),
      failed=jnp.array(False, dtype=bool),
      # algorithm begins at 1 as per Wright and Nocedal, however Scipy has a
      # bug and starts at 0. See https://github.com/scipy/scipy/issues/12157
      i=1,
      a_i1=0.,
      phi_i1=phi_0,
      dphi_i1=dphi_0,
      nfev=1 if (old_fval is None or gfk is None) else 0,
      ngev=1 if (old_fval is None or gfk is None) else 0,
      a_star=0.,
      phi_star=phi_0,
      dphi_star=dphi_0,
      g_star=gfk,
  )

  def body(state) -> _LineSearchState:
    # no amax in this version, we just double as in scipy.
    # unlike original algorithm we do our next choice at the start of this loop
    a_i = jnp.where(state.i == 1, start_value, state.a_i1 * 2.)

    phi_i, dphi_i, g_i = restricted_func_and_grad(a_i)
    state = state._replace(nfev=state.nfev + 1,
                           ngev=state.ngev + 1)

    star_to_zoom1 = wolfe_one(a_i, phi_i) | ((phi_i >= state.phi_i1) & (state.i > 1))
    star_to_i = wolfe_two(dphi_i) & (~star_to_zoom1)
    star_to_zoom2 = (dphi_i >= 0.) & (~star_to_zoom1) & (~star_to_i)

    zoom1 = _zoom(restricted_func_and_grad,
                  wolfe_one,
                  wolfe_two,
                  state.a_i1,
                  state.phi_i1,
                  state.dphi_i1,
                  a_i,
                  phi_i,
                  dphi_i,
                  gfk,
                  ~star_to_zoom1)

    state = state._replace(nfev=state.nfev + zoom1.nfev,
                           ngev=state.ngev + zoom1.ngev)

    zoom2 = _zoom(restricted_func_and_grad,
                  wolfe_one,
                  wolfe_two,
                  a_i,
                  phi_i,
                  dphi_i,
                  state.a_i1,
                  state.phi_i1,
                  state.dphi_i1,
                  gfk,
                  ~star_to_zoom2)

    state = state._replace(nfev=state.nfev + zoom2.nfev,
                           ngev=state.ngev + zoom2.ngev)

    state = state._replace(
        done=star_to_zoom1 | state.done,
        failed=(star_to_zoom1 & zoom1.failed) | state.failed,
        **_binary_replace(
            star_to_zoom1,
            state._asdict(),
            zoom1._asdict(),
            keys=['a_star', 'phi_star', 'dphi_star', 'g_star'],
        ),
    )
    state = state._replace(
        done=star_to_i | state.done,
        **_binary_replace(
            star_to_i,
            state._asdict(),
            dict(
                a_star=a_i,
                phi_star=phi_i,
                dphi_star=dphi_i,
                g_star=g_i,
            ),
        ),
    )
    state = state._replace(
        done=star_to_zoom2 | state.done,
        failed=(star_to_zoom2 & zoom2.failed) | state.failed,
        **_binary_replace(
            star_to_zoom2,
            state._asdict(),
            zoom2._asdict(),
            keys=['a_star', 'phi_star', 'dphi_star', 'g_star'],
        ),
    )
    state = state._replace(i=state.i + 1, a_i1=a_i, phi_i1=phi_i, dphi_i1=dphi_i)
    return state

  state: _LineSearchState = lax.while_loop(
    lambda state: (~state.done) & (state.i <= maxiter) & (~state.failed),
    body,
    state)

  status = jnp.where(
      state.failed,
      jnp.array(1),  # zoom failed
          jnp.where(
              state.i > maxiter,
              jnp.array(3),  # maxiter reached
              jnp.array(0),  # passed (should be)
          ),
  )
  # Step sizes which are too small causes the optimizer to get stuck with a
  # direction of zero in <64 bit mode - avoid with a floor on minimum step size.
  alpha_k = jnp.asarray(state.a_star)
  alpha_k = jnp.where((dtypes.finfo(alpha_k.dtype).bits != 64)
                    & (jnp.abs(alpha_k) < 1e-8),
                      jnp.sign(alpha_k) * 1e-8,
                      alpha_k)
  results = _LineSearchResults(
      failed=state.failed | (~state.done),
      nit=state.i - 1,  # because iterations started at 1
      nfev=state.nfev,
      ngev=state.ngev,
      k=state.i,
      a_k=alpha_k,
      f_k=state.phi_star,
      g_k=state.g_star,
      status=status,
  )
  return results

