
def test_mix_number_mult_symbols():
    assert julia_code(3*x) == "3 * x"
    assert julia_code(pi*x) == "pi * x"
    assert julia_code(3/x) == "3 ./ x"
    assert julia_code(pi/x) == "pi ./ x"
    assert julia_code(x/3) == "x / 3"
    assert julia_code(x/pi) == "x / pi"
    assert julia_code(x*y) == "x .* y"
    assert julia_code(3*x*y) == "3 * x .* y"
    assert julia_code(3*pi*x*y) == "3 * pi * x .* y"
    assert julia_code(x/y) == "x ./ y"
    assert julia_code(3*x/y) == "3 * x ./ y"
    assert julia_code(x*y/z) == "x .* y ./ z"
    assert julia_code(x/y*z) == "x .* z ./ y"
    assert julia_code(1/x/y) == "1 ./ (x .* y)"
    assert julia_code(2*pi*x/y/z) == "2 * pi * x ./ (y .* z)"
    assert julia_code(3*pi/x) == "3 * pi ./ x"
    assert julia_code(S(3)/5) == "3 // 5"
    assert julia_code(S(3)/5*x) == "(3 // 5) * x"
    assert julia_code(x/y/z) == "x ./ (y .* z)"
    assert julia_code((x+y)/z) == "(x + y) ./ z"
    assert julia_code((x+y)/(z+x)) == "(x + y) ./ (x + z)"
    assert julia_code((x+y)/EulerGamma) == "(x + y) / eulergamma"
    assert julia_code(x/3/pi) == "x / (3 * pi)"
    assert julia_code(S(3)/5*x*y/pi) == "(3 // 5) * x .* y / pi"


def test_mix_number_mult_symbols():
    assert maple_code(3 * x) == "3*x"
    assert maple_code(pi * x) == "Pi*x"
    assert maple_code(3 / x) == "3/x"
    assert maple_code(pi / x) == "Pi/x"
    assert maple_code(x / 3) == '(1/3)*x'
    assert maple_code(x / pi) == "x/Pi"
    assert maple_code(x * y) == "x*y"
    assert maple_code(3 * x * y) == "3*x*y"
    assert maple_code(3 * pi * x * y) == "3*Pi*x*y"
    assert maple_code(x / y) == "x/y"
    assert maple_code(3 * x / y) == "3*x/y"
    assert maple_code(x * y / z) == "x*y/z"
    assert maple_code(x / y * z) == "x*z/y"
    assert maple_code(1 / x / y) == "1/(x*y)"
    assert maple_code(2 * pi * x / y / z) == "2*Pi*x/(y*z)"
    assert maple_code(3 * pi / x) == "3*Pi/x"
    assert maple_code(S(3) / 5) == "3/5"
    assert maple_code(S(3) / 5 * x) == '(3/5)*x'
    assert maple_code(x / y / z) == "x/(y*z)"
    assert maple_code((x + y) / z) == "(x + y)/z"
    assert maple_code((x + y) / (z + x)) == "(x + y)/(x + z)"
    assert maple_code((x + y) / EulerGamma) == '(x + y)/gamma'
    assert maple_code(x / 3 / pi) == '(1/3)*x/Pi'
    assert maple_code(S(3) / 5 * x * y / pi) == '(3/5)*x*y/Pi'


def test_mix_number_mult_symbols():
    assert mcode(3*x) == "3*x"
    assert mcode(pi*x) == "pi*x"
    assert mcode(3/x) == "3./x"
    assert mcode(pi/x) == "pi./x"
    assert mcode(x/3) == "x/3"
    assert mcode(x/pi) == "x/pi"
    assert mcode(x*y) == "x.*y"
    assert mcode(3*x*y) == "3*x.*y"
    assert mcode(3*pi*x*y) == "3*pi*x.*y"
    assert mcode(x/y) == "x./y"
    assert mcode(3*x/y) == "3*x./y"
    assert mcode(x*y/z) == "x.*y./z"
    assert mcode(x/y*z) == "x.*z./y"
    assert mcode(1/x/y) == "1./(x.*y)"
    assert mcode(2*pi*x/y/z) == "2*pi*x./(y.*z)"
    assert mcode(3*pi/x) == "3*pi./x"
    assert mcode(S(3)/5) == "3/5"
    assert mcode(S(3)/5*x) == "3*x/5"
    assert mcode(x/y/z) == "x./(y.*z)"
    assert mcode((x+y)/z) == "(x + y)./z"
    assert mcode((x+y)/(z+x)) == "(x + y)./(x + z)"
    assert mcode((x+y)/EulerGamma) == "(x + y)/%s" % EulerGamma.evalf(17)
    assert mcode(x/3/pi) == "x/(3*pi)"
    assert mcode(S(3)/5*x*y/pi) == "3*x.*y/(5*pi)"


def test_mix_number_mult_symbols():
    with _check_warns([_W.WILL_NOT_ASSERT]) as w:
        assert smtlib_code(
            1 / pi,
            known_constants={pi: "MY_PI"},
            log_warn=w
        ) == '(pow MY_PI -1)'

    with _check_warns([_W.WILL_NOT_ASSERT]) as w:
        assert smtlib_code(
            [
                Eq(pi, 3.14, evaluate=False),
                1 / pi,
            ],
            known_constants={pi: "MY_PI"},
            log_warn=w
        ) == '(assert (= MY_PI 3.14))\n' \
             '(pow MY_PI -1)'

    with _check_warns([_W.WILL_NOT_ASSERT]) as w:
        assert smtlib_code(
            Add(S.Zero, S.One, S.NegativeOne, S.Half,
                S.Exp1, S.Pi, S.GoldenRatio, evaluate=False),
            known_constants={
                S.Pi: 'p', S.GoldenRatio: 'g',
                S.Exp1: 'e'
            },
            known_functions={
                Add: 'plus',
                exp: 'exp'
            },
            precision=3,
            log_warn=w
        ) == '(plus 0 1 -1 (/ 1 2) (exp 1) p g)'

    with _check_warns([_W.WILL_NOT_ASSERT]) as w:
        assert smtlib_code(
            Add(S.Zero, S.One, S.NegativeOne, S.Half,
                S.Exp1, S.Pi, S.GoldenRatio, evaluate=False),
            known_constants={
                S.Pi: 'p'
            },
            known_functions={
                Add: 'plus',
                exp: 'exp'
            },
            precision=3,
            log_warn=w
        ) == '(plus 0 1 -1 (/ 1 2) (exp 1) p 1.62)'

    with _check_warns([_W.WILL_NOT_ASSERT]) as w:
        assert smtlib_code(
            Add(S.Zero, S.One, S.NegativeOne, S.Half,
                S.Exp1, S.Pi, S.GoldenRatio, evaluate=False),
            known_functions={Add: 'plus'},
            precision=3,
            log_warn=w
        ) == '(plus 0 1 -1 (/ 1 2) 2.72 3.14 1.62)'

    with _check_warns([_W.WILL_NOT_ASSERT]) as w:
        assert smtlib_code(
            Add(S.Zero, S.One, S.NegativeOne, S.Half,
                S.Exp1, S.Pi, S.GoldenRatio, evaluate=False),
            known_constants={S.Exp1: 'e'},
            known_functions={Add: 'plus'},
            precision=3,
            log_warn=w
        ) == '(plus 0 1 -1 (/ 1 2) e 3.14 1.62)'

