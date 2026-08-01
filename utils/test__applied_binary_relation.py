
def test_AppliedBinaryRelation():
    with _check_warns([_W.DEFAULTING_TO_FLOAT] * 12) as w:
        assert smtlib_code(Q.eq(x, y), auto_declare=False, log_warn=w) == "(assert (= x y))"
        assert smtlib_code(Q.ne(x, y), auto_declare=False, log_warn=w) == "(assert (not (= x y)))"
        assert smtlib_code(Q.lt(x, y), auto_declare=False, log_warn=w) == "(assert (< x y))"
        assert smtlib_code(Q.le(x, y), auto_declare=False, log_warn=w) == "(assert (<= x y))"
        assert smtlib_code(Q.gt(x, y), auto_declare=False, log_warn=w) == "(assert (> x y))"
        assert smtlib_code(Q.ge(x, y), auto_declare=False, log_warn=w) == "(assert (>= x y))"

    raises(ValueError, lambda: smtlib_code(Q.complex(x), log_warn=w))


def test_AppliedBinaryRelation():
    assert str(Q.eq(x, y)) == "Q.eq(x, y)"
    assert str(Q.ne(x, y)) == "Q.ne(x, y)"

