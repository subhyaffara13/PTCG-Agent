import math


def test_Piecewise():

    modules = [math]
    if numpy:
        modules.append('numpy')

    for mod in modules:
        # test isinf
        f = lambdify(x, Piecewise((7.0, isinf(x)), (3.0, True)), mod)
        assert f(+float('inf')) == +7.0
        assert f(-float('inf')) == +7.0
        assert f(42.) == 3.0

        f2 = lambdify(x, Piecewise((7.0*sign(x), isinf(x)), (3.0, True)), mod)
        assert f2(+float('inf')) == +7.0
        assert f2(-float('inf')) == -7.0
        assert f2(42.) == 3.0

        # test isnan (gh-26784)
        g = lambdify(x, Piecewise((7.0, isnan(x)), (3.0, True)), mod)
        assert g(float('nan')) == 7.0
        assert g(42.) == 3.0


def test_Piecewise():
    f = Piecewise((-z + x*y, Eq(y, 0)), (-z - x*y, True))
    ans = cse(f)
    actual_ans = ([(x0, x*y)],
        [Piecewise((x0 - z, Eq(y, 0)), (-z - x0, True))])
    assert ans == actual_ans


def test_Piecewise():
    e1 = x*(x + y) - y*(x + y)
    e2 = sin(x)**2 + cos(x)**2
    e3 = expand((x + y)*y/x)
    s1 = simplify(e1)
    s2 = simplify(e2)
    s3 = simplify(e3)
    assert simplify(Piecewise((e1, x < e2), (e3, True))) == \
        Piecewise((s1, x < s2), (s3, True))


def test_Piecewise():
    e1 = x*(x + y) - y*(x + y)
    e2 = sin(x)**2 + cos(x)**2
    e3 = expand((x + y)*y/x)
    # s1 = simplify(e1)
    s2 = simplify(e2)
    # s3 = simplify(e3)

    # trigsimp tries not to touch non-trig containing args
    assert trigsimp(Piecewise((e1, e3 < e2), (e3, True))) == \
        Piecewise((e1, e3 < s2), (e3, True))


def test_Piecewise():
    # A piecewise linear
    expr = sy.Piecewise((0, x<0), (x, x<2), (1, True))  # ___/III
    result = aesara_code_(expr)
    assert result.owner.op == aet.switch

    expected = aet.switch(xt<0, 0, aet.switch(xt<2, xt, 1))
    assert theq(result, expected)

    expr = sy.Piecewise((x, x < 0))
    result = aesara_code_(expr)
    expected = aet.switch(xt < 0, xt, np.nan)
    assert theq(result, expected)

    expr = sy.Piecewise((0, sy.And(x>0, x<2)), \
        (x, sy.Or(x>2, x<0)))
    result = aesara_code_(expr)
    expected = aet.switch(aet.and_(xt>0,xt<2), 0, \
        aet.switch(aet.or_(xt>2, xt<0), xt, np.nan))
    assert theq(result, expected)


def test_Piecewise():
    expr = Piecewise((x, x < 1), (x + 2, True))
    assert rust_code(expr) == (
            "if (x < 1.0) {\n"
            "    x\n"
            "} else {\n"
            "    x + 2.0\n"
            "}")
    assert rust_code(expr, assign_to="r") == (
        "r = if (x < 1.0) {\n"
        "    x\n"
        "} else {\n"
        "    x + 2.0\n"
        "};")
    assert rust_code(expr, assign_to="r", inline=True) == (
        "r = if (x < 1.0) { x } else { x + 2.0 };")
    expr = Piecewise((x, x < 1), (x + 1, x < 5), (x + 2, True))
    assert rust_code(expr, inline=True) == (
        "if (x < 1.0) { x } else if (x < 5.0) { x + 1.0 } else { x + 2.0 }")
    assert rust_code(expr, assign_to="r", inline=True) == (
        "r = if (x < 1.0) { x } else if (x < 5.0) { x + 1.0 } else { x + 2.0 };")
    assert rust_code(expr, assign_to="r") == (
        "r = if (x < 1.0) {\n"
        "    x\n"
        "} else if (x < 5.0) {\n"
        "    x + 1.0\n"
        "} else {\n"
        "    x + 2.0\n"
        "};")
    expr = 2*Piecewise((x, x < 1), (x + 1, x < 5), (x + 2, True))
    assert rust_code(expr, inline=True) == (
        "2.0*if (x < 1.0) { x } else if (x < 5.0) { x + 1.0 } else { x + 2.0 }")
    expr = 2*Piecewise((x, x < 1), (x + 1, x < 5), (x + 2, True)) - 42
    assert rust_code(expr, inline=True) == (
        "2.0*if (x < 1.0) { x } else if (x < 5.0) { x + 1.0 } else { x + 2.0 } - 42.0")
    # Check that Piecewise without a True (default) condition error
    expr = Piecewise((x, x < 1), (x**2, x > 1), (sin(x), x > 0))
    raises(ValueError, lambda: rust_code(expr))


def test_Piecewise():
    # A piecewise linear
    expr = sy.Piecewise((0, x<0), (x, x<2), (1, True))  # ___/III
    result = theano_code_(expr)
    assert result.owner.op == tt.switch

    expected = tt.switch(xt<0, 0, tt.switch(xt<2, xt, 1))
    assert theq(result, expected)

    expr = sy.Piecewise((x, x < 0))
    result = theano_code_(expr)
    expected = tt.switch(xt < 0, xt, np.nan)
    assert theq(result, expected)

    expr = sy.Piecewise((0, sy.And(x>0, x<2)), \
        (x, sy.Or(x>2, x<0)))
    result = theano_code_(expr)
    expected = tt.switch(tt.and_(xt>0,xt<2), 0, \
        tt.switch(tt.or_(xt>2, xt<0), xt, np.nan))
    assert theq(result, expected)


def test_Piecewise():
    assert refine(Piecewise((1, x < 0), (3, True)), (x < 0)) == 1
    assert refine(Piecewise((1, x < 0), (3, True)), ~(x < 0)) == 3
    assert refine(Piecewise((1, x < 0), (3, True)), (y < 0)) == \
        Piecewise((1, x < 0), (3, True))
    assert refine(Piecewise((1, x > 0), (3, True)), (x > 0)) == 1
    assert refine(Piecewise((1, x > 0), (3, True)), ~(x > 0)) == 3
    assert refine(Piecewise((1, x > 0), (3, True)), (y > 0)) == \
        Piecewise((1, x > 0), (3, True))
    assert refine(Piecewise((1, x <= 0), (3, True)), (x <= 0)) == 1
    assert refine(Piecewise((1, x <= 0), (3, True)), ~(x <= 0)) == 3
    assert refine(Piecewise((1, x <= 0), (3, True)), (y <= 0)) == \
        Piecewise((1, x <= 0), (3, True))
    assert refine(Piecewise((1, x >= 0), (3, True)), (x >= 0)) == 1
    assert refine(Piecewise((1, x >= 0), (3, True)), ~(x >= 0)) == 3
    assert refine(Piecewise((1, x >= 0), (3, True)), (y >= 0)) == \
        Piecewise((1, x >= 0), (3, True))
    assert refine(Piecewise((1, Eq(x, 0)), (3, True)), (Eq(x, 0)))\
        == 1
    assert refine(Piecewise((1, Eq(x, 0)), (3, True)), (Eq(0, x)))\
        == 1
    assert refine(Piecewise((1, Eq(x, 0)), (3, True)), ~(Eq(x, 0)))\
        == 3
    assert refine(Piecewise((1, Eq(x, 0)), (3, True)), ~(Eq(0, x)))\
        == 3
    assert refine(Piecewise((1, Eq(x, 0)), (3, True)), (Eq(y, 0)))\
        == Piecewise((1, Eq(x, 0)), (3, True))
    assert refine(Piecewise((1, Ne(x, 0)), (3, True)), (Ne(x, 0)))\
        == 1
    assert refine(Piecewise((1, Ne(x, 0)), (3, True)), ~(Ne(x, 0)))\
        == 3
    assert refine(Piecewise((1, Ne(x, 0)), (3, True)), (Ne(y, 0)))\
        == Piecewise((1, Ne(x, 0)), (3, True))

