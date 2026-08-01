
def test_issue_14607():
    # issue 14607
    s, tau_c, tau_1, tau_2, phi, K = symbols(
        's, tau_c, tau_1, tau_2, phi, K')

    target = (s**2*tau_1*tau_2 + s*tau_1 + s*tau_2 + 1)/(K*s*(-phi + tau_c))

    K_C, tau_I, tau_D = symbols('K_C, tau_I, tau_D',
                                positive=True, nonzero=True)
    PID = K_C*(1 + 1/(tau_I*s) + tau_D*s)

    eq = (target - PID).together()
    eq *= denom(eq).simplify()
    eq = Poly(eq, s)
    c = eq.coeffs()

    vars = [K_C, tau_I, tau_D]
    s = solve(c, vars, dict=True)

    assert len(s) == 1

    knownsolution = {K_C: -(tau_1 + tau_2)/(K*(phi - tau_c)),
                     tau_I: tau_1 + tau_2,
                     tau_D: tau_1*tau_2/(tau_1 + tau_2)}

    for var in vars:
        assert s[0][var].simplify() == knownsolution[var].simplify()

