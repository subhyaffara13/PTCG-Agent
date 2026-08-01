
def test_U7():
    p, t = symbols('p t', real=True)
    # Exact differential => d(V(P, T)) => dV/dP DP + dV/dT DT
    # raises ValueError:  Since there is more than one variable in the
    # expression, the variable(s) of differentiation must be supplied to
    # differentiate f(p,t)
    diff(f(p, t))

