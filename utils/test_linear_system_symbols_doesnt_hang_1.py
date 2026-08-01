
def test_linear_system_symbols_doesnt_hang_1():

    def _mk_eqs(wy):
        # Equations for fitting a wy*2 - 1 degree polynomial between two points,
        # at end points derivatives are known up to order: wy - 1
        order = 2*wy - 1
        x, x0, x1 = symbols('x, x0, x1', real=True)
        y0s = symbols('y0_:{}'.format(wy), real=True)
        y1s = symbols('y1_:{}'.format(wy), real=True)
        c = symbols('c_:{}'.format(order+1), real=True)

        expr = sum(coeff*x**o for o, coeff in enumerate(c))
        eqs = []
        for i in range(wy):
            eqs.append(expr.diff(x, i).subs({x: x0}) - y0s[i])
            eqs.append(expr.diff(x, i).subs({x: x1}) - y1s[i])
        return eqs, c

    #
    # The purpose of this test is just to see that these calls don't hang. The
    # expressions returned are complicated so are not included here. Testing
    # their correctness takes longer than solving the system.
    #

    for n in range(1, 7+1):
        eqs, c = _mk_eqs(n)
        solve(eqs, c)

