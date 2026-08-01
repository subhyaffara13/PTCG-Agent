
def _solve_robertson_lsoda(use_jac, banded):

    if use_jac:
        if banded:
            jac = banded_stiff_jac
        else:
            jac = stiff_jac
    else:
        jac = None

    if banded:
        lband = 1
        uband = 2
    else:
        lband = None
        uband = None

    r = ode(stiff_f, jac)
    r.set_integrator('lsoda',
                     lband=lband, uband=uband,
                     rtol=1e-9, atol=1e-10,
                     )
    t0 = 0
    dt = 1
    tend = 10
    y0 = np.array([1.0, 1.0, 0.0, 0.0, 1.0])
    r.set_initial_value(y0, t0)

    t = [t0]
    y = [y0.copy()]
    while r.successful() and r.t < tend:
        r.integrate(r.t + dt)
        t.append(r.t)
        y.append(r.y.copy())

    # Ensure that the Jacobian was evaluated
    # iwork[12] has the number of Jacobian evaluations.
    assert r._integrator.iwork[12] > 0

    t = np.array(t)
    y = np.array(y)
    return t, y

