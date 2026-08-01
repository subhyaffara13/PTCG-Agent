
def test_sympify2():
    class A:
        def _sympy_(self):
            return Symbol("x")**3

    a = A()

    assert _sympify(a) == x**3
    assert sympify(a) == x**3
    assert a == x**3

