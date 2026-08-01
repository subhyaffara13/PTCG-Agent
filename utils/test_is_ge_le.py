
def test_is_ge_le():
    # test assumptions
    assert is_ge(x, S(0), Q.nonnegative(x)) is True
    assert is_ge(x, S(0), Q.negative(x)) is False

    # test registration
    class PowTest(Expr):
        def __new__(cls, base, exp):
            return Basic.__new__(cls, _sympify(base), _sympify(exp))

    @dispatch(PowTest, PowTest)
    def _eval_is_ge(lhs, rhs):
        if type(lhs) == PowTest and type(rhs) == PowTest:
            return fuzzy_and([is_ge(lhs.args[0], rhs.args[0]), is_ge(lhs.args[1], rhs.args[1])])

    assert is_ge(PowTest(3, 9), PowTest(3,2))
    assert is_gt(PowTest(3, 9), PowTest(3,2))
    assert is_le(PowTest(3, 2), PowTest(3,9))
    assert is_lt(PowTest(3, 2), PowTest(3,9))

