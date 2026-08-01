
def test_issue_22523():
    N, s = symbols('N s')
    rho = Function('rho')
    # intentionally use 4.0 to confirm issue with nfloat
    # works here
    eqn = 4.0*N*sqrt(N - 1)*rho(s) + (4*s**2*(N - 1) + (N - 2*s*(N - 1))**2
        )*Derivative(rho(s), (s, 2))
    match = classify_ode(eqn, dict=True, hint='all')
    assert match['2nd_power_series_ordinary']['terms'] == 5
    C1, C2 = symbols('C1,C2')
    sol = dsolve(eqn, hint='2nd_power_series_ordinary')
    # there is no r(2.0) in this result
    assert filldedent(sol) == filldedent(str('''
        Eq(rho(s), C2*(1 - 4.0*s**4*sqrt(N - 1.0)/N + 0.666666666666667*s**4/N
        - 2.66666666666667*s**3*sqrt(N - 1.0)/N - 2.0*s**2*sqrt(N - 1.0)/N +
        9.33333333333333*s**4*sqrt(N - 1.0)/N**2 - 0.666666666666667*s**4/N**2
        + 2.66666666666667*s**3*sqrt(N - 1.0)/N**2 -
        5.33333333333333*s**4*sqrt(N - 1.0)/N**3) + C1*s*(1.0 -
        1.33333333333333*s**3*sqrt(N - 1.0)/N - 0.666666666666667*s**2*sqrt(N
        - 1.0)/N + 1.33333333333333*s**3*sqrt(N - 1.0)/N**2) + O(s**6))'''))

