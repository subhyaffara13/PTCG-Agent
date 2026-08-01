
def root_rati(f, p0, bracket, acc, maxit=MAXIT):
    """Solve `f(p) = 0` using a rational function approximation.

    In a nutshell, since the function f(p) is known to be monotonically decreasing, we
       - maintain the bracket (p1, f1), (p2, f2) and (p3, f3)
       - at each iteration step, approximate f(p) by a rational function
         r(p) = (u*p + v) / (p + w)
         and make a step to p_new to the root of f(p): r(p_new) = 0.
         The coefficients u, v and w are found from the bracket values p1..3 and f1...3

    The algorithm and implementation follows
    https://github.com/scipy/scipy/blob/maintenance/1.11.x/scipy/interpolate/fitpack/fpcurf.f#L229
    and
    https://github.com/scipy/scipy/blob/maintenance/1.11.x/scipy/interpolate/fitpack/fppara.f#L290

    Note that the latter is for parametric splines and the former is for 1D spline
    functions. The minimization is indentical though [modulo a summation over the
    dimensions in the computation of f(p)], so we reuse the minimizer for both
    d=1 and d>1.
    """
    # Magic values from
    # https://github.com/scipy/scipy/blob/maintenance/1.11.x/scipy/interpolate/fitpack/fpcurf.f#L27
    con1 = 0.1
    con9 = 0.9
    con4 = 0.04

    # bracketing flags (follow FITPACK)
    # https://github.com/scipy/scipy/blob/maintenance/1.11.x/scipy/interpolate/fitpack/fppara.f#L365
    ich1, ich3 = 0, 0

    (p1, f1), (p3, f3)  = bracket
    p = p0

    for it in range(maxit):
        p2, f2 = p, f(p)

        # c  test whether the approximation sp(x) is an acceptable solution.
        if abs(f2) < acc:
            ier, converged = 0, True
            break

        # c  carry out one more step of the iteration process.
        if ich3 == 0:
            if f2 - f3 <= acc:
                # c  our initial choice of p is too large.
                p3 = p2
                f3 = f2
                p = p*con4
                if p <= p1:
                    p = p1*con9 + p2*con1
                continue
            else:
                if f2 < 0:
                    ich3 = 1

        if ich1 == 0:
            if f1 - f2 <= acc:
                # c  our initial choice of p is too small
                p1 = p2
                f1 = f2
                p = p/con4
                if p3 != np.inf and p <= p3:
                    p = p2*con1 + p3*con9
                continue
            else:
                if f2 > 0:
                    ich1 = 1

        # c  test whether the iteration process proceeds as theoretically expected.
        # [f(p) should be monotonically decreasing]
        if f1 <= f2 or f2 <= f3:
            ier, converged = 2, False
            break

        # actually make the iteration step
        p = fprati(p1, f1, p2, f2, p3, f3)

        # c  adjust the value of p1,f1,p3 and f3 such that f1 > 0 and f3 < 0.
        if f2 < 0:
            p3, f3 = p2, f2
        else:
            p1, f1 = p2, f2

    else:
        # not converged in MAXIT iterations
        ier, converged = 3, False

    if ier != 0:
        warnings.warn(RuntimeWarning(_iermesg[ier]), stacklevel=2)

    return Bunch(converged=converged, root=p, iterations=it, ier=ier)

