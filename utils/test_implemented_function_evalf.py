
def test_implemented_function_evalf():
    from sympy.utilities.lambdify import implemented_function
    f = Function('f')
    f = implemented_function(f, lambda x: x + 1)
    assert str(f(x)) == "f(x)"
    assert str(f(2)) == "f(2)"
    assert f(2).evalf() == 3.0
    assert f(x).evalf() == f(x)
    f = implemented_function(Function('sin'), lambda x: x + 1)
    assert f(2).evalf() != sin(2)
    del f._imp_     # XXX: due to caching _imp_ would influence all other tests

