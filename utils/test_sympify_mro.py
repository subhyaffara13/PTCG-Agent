
def test_sympify_mro():
    """Tests the resolution order for classes that implement _sympy_"""
    class a:
        def _sympy_(self):
            return Integer(1)
    class b(a):
        def _sympy_(self):
            return Integer(2)
    class c(a):
        pass

    assert sympify(a()) == Integer(1)
    assert sympify(b()) == Integer(2)
    assert sympify(c()) == Integer(1)

