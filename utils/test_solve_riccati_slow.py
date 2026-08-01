
def test_solve_riccati_slow():
    """
    This function tests the computation of rational
    particular solutions for a Riccati ODE.

    Each test case has 2 values -

    1. eq - Riccati ODE to be solved.
    2. sol - Expected solution to the equation.
    """
    C0 = Dummy('C0')
    tests = [
    # Very large values of m (989 and 991)
    (
        Eq(f(x).diff(x), (1 - x)*f(x)/(x - 3) + (2 - 12*x)*f(x)**2/(2*x - 9) + \
            (54924*x**3 - 405264*x**2 + 1084347*x - 1087533)/(8*x**4 - 132*x**3 + 810*x**2 - \
            2187*x + 2187) + 495),
        [Eq(f(x), (18*x + 6)/(2*x - 9))]
    )]
    for eq, sol in tests:
        check_dummy_sol(eq, sol, C0)

