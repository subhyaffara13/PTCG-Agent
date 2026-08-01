
def test_exp_adjoint():
    x = Symbol('x', commutative=False)
    assert adjoint(exp(x)) == exp(adjoint(x))

