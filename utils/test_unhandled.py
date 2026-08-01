
def test_unhandled():
    class MyExpr(Expr):
        def _eval_derivative(self, s):
            if not s.name.startswith('xi'):
                return self
            else:
                return None

    eq = MyExpr(f(x), y, z)
    assert diff(eq, x, y, f(x), z) == Derivative(eq, f(x))
    assert diff(eq, f(x), x) == Derivative(eq, f(x))
    assert f(x, y).diff(x,(y, z)) == Derivative(f(x, y), x, (y, z))
    assert f(x, y).diff(x,(y, 0)) == Derivative(f(x, y), x)

