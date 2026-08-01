
def test_recurse_Application_args():
    F = Lambda((x, y), exp(2*x + 3*y))
    f = Function('f')
    A = f(x, f(x, x))
    C = F(x, F(x, x))
    assert A.subs(f, F) == A.replace(f, F) == C

