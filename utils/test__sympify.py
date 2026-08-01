
def test__sympify():
    x = Symbol('x')
    f = Function('f')

    # positive _sympify
    assert _sympify(x) is x
    assert _sympify(1) == Integer(1)
    assert _sympify(0.5) == Float("0.5")
    assert _sympify(1 + 1j) == 1.0 + I*1.0

    # Function f is not Basic and can't sympify to Basic. We allow it to pass
    # with sympify but not with _sympify.
    # https://github.com/sympy/sympy/issues/20124
    assert sympify(f) is f
    raises(SympifyError, lambda: _sympify(f))

    class A:
        def _sympy_(self):
            return Integer(5)

    a = A()
    assert _sympify(a) == Integer(5)

    # negative _sympify
    raises(SympifyError, lambda: _sympify('1'))
    raises(SympifyError, lambda: _sympify([1, 2, 3]))

