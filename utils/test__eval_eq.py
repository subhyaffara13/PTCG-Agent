
def test_EvalEq():
    """

    This test exists to ensure backwards compatibility.
    The method to use is _eval_is_eq
    """
    from sympy.core.expr import Expr

    class PowTest(Expr):
        def __new__(cls, base, exp):
            return Basic.__new__(PowTest, _sympify(base), _sympify(exp))

        def _eval_Eq(lhs, rhs):
            if type(lhs) == PowTest and type(rhs) == PowTest:
                return lhs.args[0] == rhs.args[0] and lhs.args[1] == rhs.args[1]

    assert is_eq(PowTest(3, 4), PowTest(3,4))
    assert is_eq(PowTest(3, 4), _sympify(4)) is None
    assert is_neq(PowTest(3, 4), PowTest(3,7))

