
def test_function_assumptions():
    x = Symbol('x')
    f = Function('f')
    f_real = Function('f', real=True)
    f_real1 = Function('f', real=1)
    f_real_inherit = Function(Symbol('f', real=True))

    assert f_real == f_real1  # assumptions are sanitized
    assert f != f_real
    assert f(x) != f_real(x)

    assert f(x).is_real is None
    assert f_real(x).is_real is True
    assert f_real_inherit(x).is_real is True and f_real_inherit.name == 'f'

    # Can also do it this way, but it won't be equal to f_real because of the
    # way UndefinedFunction.__new__ works. Any non-recognized assumptions
    # are just added literally as something which is used in the hash
    f_real2 = Function('f', is_real=True)
    assert f_real2(x).is_real is True

