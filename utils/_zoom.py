
def _zoom(a_lo, a_hi, phi_lo, phi_hi, derphi_lo,
          phi, derphi, phi0, derphi0, c1, c2, extra_condition):
    """Zoom stage of approximate linesearch satisfying strong Wolfe conditions.

    Part of the optimization algorithm in `scalar_search_wolfe2`.

    Notes
    -----
    Implements Algorithm 3.6 (zoom) in Wright and Nocedal,
    'Numerical Optimization', 1999, pp. 61.

    """

    maxiter = 10
    i = 0
    delta1 = 0.2  # cubic interpolant check
    delta2 = 0.1  # quadratic interpolant check
    phi_rec = phi0
    a_rec = 0
    while True:
        # interpolate to find a trial step length between a_lo and
        # a_hi Need to choose interpolation here. Use cubic
        # interpolation and then if the result is within delta *
        # dalpha or outside of the interval bounded by a_lo or a_hi
        # then use quadratic interpolation, if the result is still too
        # close, then use bisection

        dalpha = a_hi - a_lo
        if dalpha < 0:
            a, b = a_hi, a_lo
        else:
            a, b = a_lo, a_hi

        # minimizer of cubic interpolant
        # (uses phi_lo, derphi_lo, phi_hi, and the most recent value of phi)
        #
        # if the result is too close to the end points (or out of the
        # interval), then use quadratic interpolation with phi_lo,
        # derphi_lo and phi_hi if the result is still too close to the
        # end points (or out of the interval) then use bisection

        if (i > 0):
            cchk = delta1 * dalpha
            a_j = _cubicmin(a_lo, phi_lo, derphi_lo, a_hi, phi_hi,
                            a_rec, phi_rec)
        if (i == 0) or (a_j is None) or (a_j > b - cchk) or (a_j < a + cchk):
            qchk = delta2 * dalpha
            a_j = _quadmin(a_lo, phi_lo, derphi_lo, a_hi, phi_hi)
            if (a_j is None) or (a_j > b-qchk) or (a_j < a+qchk):
                a_j = a_lo + 0.5*dalpha

        # Check new value of a_j

        phi_aj = phi(a_j)
        if (phi_aj > phi0 + c1*a_j*derphi0) or (phi_aj >= phi_lo):
            phi_rec = phi_hi
            a_rec = a_hi
            a_hi = a_j
            phi_hi = phi_aj
        else:
            derphi_aj = derphi(a_j)
            if abs(derphi_aj) <= -c2*derphi0 and extra_condition(a_j, phi_aj):
                a_star = a_j
                val_star = phi_aj
                valprime_star = derphi_aj
                break
            if derphi_aj*(a_hi - a_lo) >= 0:
                phi_rec = phi_hi
                a_rec = a_hi
                a_hi = a_lo
                phi_hi = phi_lo
            else:
                phi_rec = phi_lo
                a_rec = a_lo
            a_lo = a_j
            phi_lo = phi_aj
            derphi_lo = derphi_aj
        i += 1
        if (i > maxiter):
            # Failed to find a conforming step size
            a_star = None
            val_star = None
            valprime_star = None
            break
    return a_star, val_star, valprime_star


def _zoom(restricted_func_and_grad, wolfe_one: ConditionFn, wolfe_two: ConditionFn, a_lo, phi_lo,
          dphi_lo, a_hi, phi_hi, dphi_hi, g_0, pass_through):
  """
  Implementation of zoom. Algorithm 3.6 from Wright and Nocedal, 'Numerical
  Optimization', 1999, pg. 59-61. Tries cubic, quadratic, and bisection methods
  of zooming.
  """
  state = _ZoomState(
      done=False,
      failed=False,
      j=0,
      a_lo=a_lo,
      phi_lo=phi_lo,
      dphi_lo=dphi_lo,
      a_hi=a_hi,
      phi_hi=phi_hi,
      dphi_hi=dphi_hi,
      a_rec=(a_lo + a_hi) / 2.,
      phi_rec=(phi_lo + phi_hi) / 2.,
      a_star=1.,
      phi_star=phi_lo,
      dphi_star=dphi_lo,
      g_star=g_0,
      nfev=0,
      ngev=0,
  )
  delta1 = 0.2
  delta2 = 0.1

  def body(state):
    # Body of zoom algorithm. We use boolean arithmetic to avoid using jax.cond
    # so that it works on GPU/TPU.
    dalpha = (state.a_hi - state.a_lo)
    a = jnp.minimum(state.a_hi, state.a_lo)
    b = jnp.maximum(state.a_hi, state.a_lo)
    cchk = delta1 * dalpha
    qchk = delta2 * dalpha

    # This will cause the line search to stop, and since the Wolfe conditions
    # are not satisfied the minimization should stop too.
    threshold = jnp.where((dtypes.finfo(dalpha.dtype).bits < 64), 1e-5, 1e-10)
    state = state._replace(failed=state.failed | (dalpha <= threshold))

    # Cubmin is sometimes nan, though in this case the bounds check will fail.
    a_j_cubic = _cubicmin(state.a_lo, state.phi_lo, state.dphi_lo, state.a_hi,
                          state.phi_hi, state.a_rec, state.phi_rec)
    use_cubic = (state.j > 0) & (a_j_cubic > a + cchk) & (a_j_cubic < b - cchk)
    a_j_quad = _quadmin(state.a_lo, state.phi_lo, state.dphi_lo, state.a_hi, state.phi_hi)
    use_quad = (~use_cubic) & (a_j_quad > a + qchk) & (a_j_quad < b - qchk)
    a_j_bisection = (state.a_lo + state.a_hi) / 2.
    use_bisection = (~use_cubic) & (~use_quad)

    a_j = jnp.where(use_cubic, a_j_cubic, state.a_rec)
    a_j = jnp.where(use_quad, a_j_quad, a_j)
    a_j = jnp.where(use_bisection, a_j_bisection, a_j)

    # TODO(jakevdp): should we use some sort of fixed-point approach here instead?
    phi_j, dphi_j, g_j = restricted_func_and_grad(a_j)
    phi_j = phi_j.astype(state.phi_lo.dtype)
    dphi_j = dphi_j.astype(state.dphi_lo.dtype)
    g_j = g_j.astype(state.g_star.dtype)
    state = state._replace(nfev=state.nfev + 1,
                           ngev=state.ngev + 1)

    hi_to_j = wolfe_one(a_j, phi_j) | (phi_j >= state.phi_lo)
    star_to_j = wolfe_two(dphi_j) & (~hi_to_j)
    hi_to_lo = (dphi_j * (state.a_hi - state.a_lo) >= 0.) & (~hi_to_j) & (~star_to_j)
    lo_to_j = (~hi_to_j) & (~star_to_j)

    state = state._replace(
        **_binary_replace(
            hi_to_j,
            state._asdict(),
            dict(
                a_hi=a_j,
                phi_hi=phi_j,
                dphi_hi=dphi_j,
                a_rec=state.a_hi,
                phi_rec=state.phi_hi,
            ),
        ),
    )

    # for termination
    state = state._replace(
        done=star_to_j | state.done,
        **_binary_replace(
            star_to_j,
            state._asdict(),
            dict(
                a_star=a_j,
                phi_star=phi_j,
                dphi_star=dphi_j,
                g_star=g_j,
            )
        ),
    )
    state = state._replace(
        **_binary_replace(
            hi_to_lo,
            state._asdict(),
            dict(
                a_hi=state.a_lo,
                phi_hi=state.phi_lo,
                dphi_hi=state.dphi_lo,
                a_rec=state.a_hi,
                phi_rec=state.phi_hi,
            ),
        ),
    )
    state = state._replace(
        **_binary_replace(
            lo_to_j & ~hi_to_lo,
            state._asdict(),
            dict(
                a_rec=state.a_lo,
                phi_rec=state.phi_lo,
            ),
        ),
    )
    state = state._replace(
        **_binary_replace(
            lo_to_j,
            state._asdict(),
            dict(
                a_lo=a_j,
                phi_lo=phi_j,
                dphi_lo=dphi_j,
            ),
        ),
    )
    state = state._replace(j=state.j + 1)
    # Choose higher cutoff for maxiter than Scipy as Jax takes longer to find
    # the same value - possibly floating point issues?
    state = state._replace(failed= state.failed | (state.j >= 30))
    return state

  state = lax.while_loop(lambda state: (~state.done) & (~pass_through) & (~state.failed),
                         body,
                         state)

  return state

