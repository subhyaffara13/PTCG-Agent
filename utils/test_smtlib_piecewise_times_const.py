
def test_smtlib_piecewise_times_const():
    pw = Piecewise((x, x < 1), (x ** 2, True))
    with _check_warns([_W.DEFAULTING_TO_FLOAT, _W.WILL_NOT_ASSERT]) as w:
        assert smtlib_code(2 * pw, log_warn=w) == '(declare-const x Real)\n(* 2 (ite (< x 1) x (pow x 2)))'
    with _check_warns([_W.DEFAULTING_TO_FLOAT, _W.WILL_NOT_ASSERT]) as w:
        assert smtlib_code(pw / x, log_warn=w) == '(declare-const x Real)\n(* (pow x -1) (ite (< x 1) x (pow x 2)))'
    with _check_warns([_W.DEFAULTING_TO_FLOAT, _W.DEFAULTING_TO_FLOAT, _W.WILL_NOT_ASSERT]) as w:
        assert smtlib_code(pw / (x * y), log_warn=w) == '(declare-const x Real)\n(declare-const y Real)\n(* (pow x -1) (pow y -1) (ite (< x 1) x (pow x 2)))'
    with _check_warns([_W.DEFAULTING_TO_FLOAT, _W.WILL_NOT_ASSERT]) as w:
        assert smtlib_code(pw / 3, log_warn=w) == '(declare-const x Real)\n(* (/ 1 3) (ite (< x 1) x (pow x 2)))'

