
def test_AppliedPredicate():
    sT(Q.even(Symbol('z')), "AppliedPredicate(Q.even, Symbol('z'))")


def test_AppliedPredicate():
    with _check_warns([_W.DEFAULTING_TO_FLOAT] * 6) as w:
        assert smtlib_code(Q.positive(x), auto_declare=False, log_warn=w) == "(assert (> x 0))"
        assert smtlib_code(Q.negative(x), auto_declare=False, log_warn=w) == "(assert (< x 0))"
        assert smtlib_code(Q.zero(x), auto_declare=False, log_warn=w) == "(assert (= x 0))"
        assert smtlib_code(Q.nonpositive(x), auto_declare=False, log_warn=w) == "(assert (<= x 0))"
        assert smtlib_code(Q.nonnegative(x), auto_declare=False, log_warn=w) == "(assert (>= x 0))"
        assert smtlib_code(Q.nonzero(x), auto_declare=False, log_warn=w) == "(assert (not (= x 0)))"


def test_AppliedPredicate():
    assert sstr(Q.even(x)) == 'Q.even(x)'

