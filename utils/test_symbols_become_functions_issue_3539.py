
def test_symbols_become_functions_issue_3539():
    from sympy.abc import alpha, phi, beta, t
    raises(TypeError, lambda: beta(2))
    raises(TypeError, lambda: beta(2.5))
    raises(TypeError, lambda: phi(2.5))
    raises(TypeError, lambda: alpha(2.5))
    raises(TypeError, lambda: phi(t))

