
def test_piecewise():
    # https://github.com/sympy/sympy/issues/18363
    assert limit((real_root(x - 6, 3) + 2)/(x + 2), x, -2, '+') == Rational(1, 12)


def test_piecewise():
    # In each case, test eval() the lambdarepr() to make sure there are a
    # correct number of parentheses. It will give a SyntaxError if there aren't.

    h = "lambda x: "

    p = Piecewise((x, x < 0))
    l = lambdarepr(p)
    eval(h + l)
    assert l == "((x) if (x < 0) else None)"

    p = Piecewise(
        (1, x < 1),
        (2, x < 2),
        (0, True)
    )
    l = lambdarepr(p)
    eval(h + l)
    assert l == "((1) if (x < 1) else (2) if (x < 2) else (0))"

    p = Piecewise(
        (1, x < 1),
        (2, x < 2),
    )
    l = lambdarepr(p)
    eval(h + l)
    assert l == "((1) if (x < 1) else (2) if (x < 2) else None)"

    p = Piecewise(
        (x, x < 1),
        (x**2, Interval(3, 4, True, False).contains(x)),
        (0, True),
    )
    l = lambdarepr(p)
    eval(h + l)
    assert l == "((x) if (x < 1) else (x**2) if (((x <= 4)) and ((x > 3))) else (0))"

    p = Piecewise(
        (x**2, x < 0),
        (x, x < 1),
        (2 - x, x >= 1),
        (0, True), evaluate=False
    )
    l = lambdarepr(p)
    eval(h + l)
    assert l == "((x**2) if (x < 0) else (x) if (x < 1)"\
                                " else (2 - x) if (x >= 1) else (0))"

    p = Piecewise(
        (x**2, x < 0),
        (x, x < 1),
        (2 - x, x >= 1), evaluate=False
    )
    l = lambdarepr(p)
    eval(h + l)
    assert l == "((x**2) if (x < 0) else (x) if (x < 1)"\
                    " else (2 - x) if (x >= 1) else None)"

    p = Piecewise(
        (1, x >= 1),
        (2, x >= 2),
        (3, x >= 3),
        (4, x >= 4),
        (5, x >= 5),
        (6, True)
    )
    l = lambdarepr(p)
    eval(h + l)
    assert l == "((1) if (x >= 1) else (2) if (x >= 2) else (3) if (x >= 3)"\
                        " else (4) if (x >= 4) else (5) if (x >= 5) else (6))"

    p = Piecewise(
        (1, x <= 1),
        (2, x <= 2),
        (3, x <= 3),
        (4, x <= 4),
        (5, x <= 5),
        (6, True)
    )
    l = lambdarepr(p)
    eval(h + l)
    assert l == "((1) if (x <= 1) else (2) if (x <= 2) else (3) if (x <= 3)"\
                            " else (4) if (x <= 4) else (5) if (x <= 5) else (6))"

    p = Piecewise(
        (1, x > 1),
        (2, x > 2),
        (3, x > 3),
        (4, x > 4),
        (5, x > 5),
        (6, True)
    )
    l = lambdarepr(p)
    eval(h + l)
    assert l =="((1) if (x > 1) else (2) if (x > 2) else (3) if (x > 3)"\
                            " else (4) if (x > 4) else (5) if (x > 5) else (6))"

    p = Piecewise(
        (1, x < 1),
        (2, x < 2),
        (3, x < 3),
        (4, x < 4),
        (5, x < 5),
        (6, True)
    )
    l = lambdarepr(p)
    eval(h + l)
    assert l == "((1) if (x < 1) else (2) if (x < 2) else (3) if (x < 3)"\
                            " else (4) if (x < 4) else (5) if (x < 5) else (6))"

    p = Piecewise(
        (Piecewise(
            (1, x > 0),
            (2, True)
        ), y > 0),
        (3, True)
    )
    l = lambdarepr(p)
    eval(h + l)
    assert l == "((((1) if (x > 0) else (2))) if (y > 0) else (3))"

