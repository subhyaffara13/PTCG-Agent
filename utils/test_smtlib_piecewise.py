
def test_smtlib_piecewise():
    with _check_warns([_W.DEFAULTING_TO_FLOAT, _W.WILL_NOT_ASSERT]) as w:
        assert smtlib_code(
            Piecewise((x, x < 1),
                      (x ** 2, True)),
            auto_declare=False,
            log_warn=w
        ) == '(ite (< x 1) x (pow x 2))'

    with _check_warns([_W.DEFAULTING_TO_FLOAT, _W.WILL_NOT_ASSERT]) as w:
        assert smtlib_code(
            Piecewise((x ** 2, x < 1),
                      (x ** 3, x < 2),
                      (x ** 4, x < 3),
                      (x ** 5, True)),
            auto_declare=False,
            log_warn=w
        ) == '(ite (< x 1) (pow x 2) ' \
             '(ite (< x 2) (pow x 3) ' \
             '(ite (< x 3) (pow x 4) ' \
             '(pow x 5))))'

    # Check that Piecewise without a True (default) condition error
    expr = Piecewise((x, x < 1), (x ** 2, x > 1), (sin(x), x > 0))
    with _check_warns([_W.DEFAULTING_TO_FLOAT, _W.WILL_NOT_ASSERT]) as w:
        raises(AssertionError, lambda: smtlib_code(expr, log_warn=w))

