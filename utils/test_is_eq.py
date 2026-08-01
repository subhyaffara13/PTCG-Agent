
def test_is_eq():
    # test assumptions
    assert is_eq(x, y, Q.infinite(x) & Q.finite(y)) is False
    assert is_eq(x, y, Q.infinite(x) & Q.infinite(y) & Q.extended_real(x) & ~Q.extended_real(y)) is False
    assert is_eq(x, y, Q.infinite(x) & Q.infinite(y) & Q.extended_positive(x) & Q.extended_negative(y)) is False

    assert is_eq(x+I, y+I, Q.infinite(x) & Q.finite(y)) is False
    assert is_eq(1+x*I, 1+y*I, Q.infinite(x) & Q.finite(y)) is False

    assert is_eq(x, S(0), assumptions=Q.zero(x))
    assert is_eq(x, S(0), assumptions=~Q.zero(x)) is False
    assert is_eq(x, S(0), assumptions=Q.nonzero(x)) is False
    assert is_neq(x, S(0), assumptions=Q.zero(x)) is False
    assert is_neq(x, S(0), assumptions=~Q.zero(x))
    assert is_neq(x, S(0), assumptions=Q.nonzero(x))

    # test registration
    class PowTest(Expr):
        def __new__(cls, base, exp):
            return Basic.__new__(cls, _sympify(base), _sympify(exp))

    @dispatch(PowTest, PowTest)
    def _eval_is_eq(lhs, rhs):
        if type(lhs) == PowTest and type(rhs) == PowTest:
            return fuzzy_and([is_eq(lhs.args[0], rhs.args[0]), is_eq(lhs.args[1], rhs.args[1])])

    assert is_eq(PowTest(3, 4), PowTest(3,4))
    assert is_eq(PowTest(3, 4), _sympify(4)) is None
    assert is_neq(PowTest(3, 4), PowTest(3,7))

