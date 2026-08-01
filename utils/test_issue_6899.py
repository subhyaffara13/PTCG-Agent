
def test_issue_6899():
    from sympy.core.function import Lambda
    x = Symbol('x')
    eqn = Lambda(x, x)
    assert eqn.func(*eqn.args) == eqn

