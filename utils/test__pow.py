
def test_Pow():
    assert (SetExpr(Interval(0, 2))**2).set == Interval(0, 4)


def test_Pow():
    assert julia_code(x**3) == "x .^ 3"
    assert julia_code(x**(y**3)) == "x .^ (y .^ 3)"
    assert julia_code(x**Rational(2, 3)) == 'x .^ (2 // 3)'
    g = implemented_function('g', Lambda(x, 2*x))
    assert julia_code(1/(g(x)*3.5)**(x - y**x)/(x**2 + y)) == \
        "(3.5 * 2 * x) .^ (-x + y .^ x) ./ (x .^ 2 + y)"
    # For issue 14160
    assert julia_code(Mul(-2, x, Pow(Mul(y,y,evaluate=False), -1, evaluate=False),
                                                evaluate=False)) == '-2 * x ./ (y .* y)'


def test_Pow():
    e = Pow(2, 2, evaluate=False)
    assert latex(e) == r'2^{2}'
    assert latex(x**(Rational(-1, 3))) == r'\frac{1}{\sqrt[3]{x}}'
    x2 = Symbol(r'x^2')
    assert latex(x2**2) == r'\left(x^{2}\right)^{2}'
    # Issue 11011
    assert latex(S('1.453e4500')**x) == r'{1.453 \cdot 10^{4500}}^{x}'


def test_Pow():
    assert maple_code(x ** 3) == "x^3"
    assert maple_code(x ** (y ** 3)) == "x^(y^3)"

    assert maple_code((x ** 3) ** y) == "(x^3)^y"
    assert maple_code(x ** Rational(2, 3)) == 'x^(2/3)'

    g = implemented_function('g', Lambda(x, 2 * x))
    assert maple_code(1 / (g(x) * 3.5) ** (x - y ** x) / (x ** 2 + y)) == \
           "(3.5*2*x)^(-x + y^x)/(x^2 + y)"
    # For issue 14160
    assert maple_code(Mul(-2, x, Pow(Mul(y, y, evaluate=False), -1, evaluate=False),
                          evaluate=False)) == '-2*x/(y*y)'


def test_Pow():
    assert mcode(x**3) == "x^3"
    assert mcode(x**(y**3)) == "x^(y^3)"
    assert mcode(1/(f(x)*3.5)**(x - y**x)/(x**2 + y)) == \
        "(3.5*f[x])^(-x + y^x)/(x^2 + y)"
    assert mcode(x**-1.0) == 'x^(-1.0)'
    assert mcode(x**Rational(2, 3)) == 'x^(2/3)'


def test_Pow():
    assert mcode(x**3) == "x.^3"
    assert mcode(x**(y**3)) == "x.^(y.^3)"
    assert mcode(x**Rational(2, 3)) == 'x.^(2/3)'
    g = implemented_function('g', Lambda(x, 2*x))
    assert mcode(1/(g(x)*3.5)**(x - y**x)/(x**2 + y)) == \
        "(3.5*2*x).^(-x + y.^x)./(x.^2 + y)"
    # For issue 14160
    assert mcode(Mul(-2, x, Pow(Mul(y,y,evaluate=False), -1, evaluate=False),
                                                evaluate=False)) == '-2*x./(y.*y)'


def test_Pow():
    assert precedence(x**y) == PRECEDENCE["Pow"]
    assert precedence(-x**y) == PRECEDENCE["Add"]
    assert precedence(x**-y) == PRECEDENCE["Pow"]


def test_Pow():
    assert rust_code(1/x) == "x.recip()"
    assert rust_code(x**-1) == rust_code(x**-1.0) == "x.recip()"
    assert rust_code(sqrt(x)) == "x.sqrt()"
    assert rust_code(x**S.Half) == rust_code(x**0.5) == "x.sqrt()"

    assert rust_code(1/sqrt(x)) == "x.sqrt().recip()"
    assert rust_code(x**-S.Half) == rust_code(x**-0.5) == "x.sqrt().recip()"

    assert rust_code(1/pi) == "PI.recip()"
    assert rust_code(pi**-1) == rust_code(pi**-1.0) == "PI.recip()"
    assert rust_code(pi**-0.5) == "PI.sqrt().recip()"

    assert rust_code(x**Rational(1, 3)) == "x.cbrt()"
    assert rust_code(2**x) == "x.exp2()"
    assert rust_code(exp(x)) == "x.exp()"
    assert rust_code(x**3) == "x.powi(3)"
    assert rust_code(x**(y**3)) == "x.powf(y.powi(3))"
    assert rust_code(x**Rational(2, 3)) == "x.powf(2_f64/3.0)"

    g = implemented_function('g', Lambda(x, 2*x))
    assert rust_code(1/(g(x)*3.5)**(x - y**x)/(x**2 + y)) == \
        "(3.5*2.0*x).powf(-x + y.powf(x))/(x.powi(2) + y)"
    _cond_cfunc = [(lambda base, exp: exp.is_integer, "dpowi", 1),
                   (lambda base, exp: not exp.is_integer, "pow", 1)]
    assert rust_code(x**3, user_functions={'Pow': _cond_cfunc}) == 'x.dpowi(3)'
    assert rust_code(x**3.2, user_functions={'Pow': _cond_cfunc}) == 'x.pow(3.2)'


def test_Pow():
    with _check_warns([_W.DEFAULTING_TO_FLOAT, _W.WILL_NOT_ASSERT]) as w:
        assert smtlib_code(x ** 3, auto_declare=False, log_warn=w) == "(pow x 3)"
    with _check_warns([_W.DEFAULTING_TO_FLOAT, _W.DEFAULTING_TO_FLOAT, _W.WILL_NOT_ASSERT]) as w:
        assert smtlib_code(x ** (y ** 3), auto_declare=False, log_warn=w) == "(pow x (pow y 3))"
    with _check_warns([_W.DEFAULTING_TO_FLOAT, _W.WILL_NOT_ASSERT]) as w:
        assert smtlib_code(x ** Rational(2, 3), auto_declare=False, log_warn=w) == '(pow x (/ 2 3))'

        a = Symbol('a', integer=True)
        b = Symbol('b', real=True)
        c = Symbol('c')

        def g(x): return 2 * x

        # if x=1, y=2, then expr=2.333...
        expr = 1 / (g(a) * 3.5) ** (a - b ** a) / (a ** 2 + b)

    with _check_warns([]) as w:
        assert smtlib_code(
            [
                Eq(a < 2, c),
                Eq(b > a, c),
                c & True,
                Eq(expr, 2 + Rational(1, 3))
            ],
            log_warn=w
        ) == '(declare-const a Int)\n' \
             '(declare-const b Real)\n' \
             '(declare-const c Bool)\n' \
             '(assert (= (< a 2) c))\n' \
             '(assert (= (> b a) c))\n' \
             '(assert c)\n' \
             '(assert (= ' \
             '(* (pow (* 7.0 a) (+ (pow b a) (* -1 a))) (pow (+ b (pow a 2)) -1)) ' \
             '(/ 7 3)' \
             '))'

    with _check_warns([_W.DEFAULTING_TO_FLOAT, _W.WILL_NOT_ASSERT]) as w:
        assert smtlib_code(
            Mul(-2, c, Pow(Mul(b, b, evaluate=False), -1, evaluate=False), evaluate=False),
            log_warn=w
        ) == '(declare-const b Real)\n' \
             '(declare-const c Real)\n' \
             '(* -2 c (pow (* b b) -1))'


def test_Pow():
    assert str(x**-1) == "1/x"
    assert str(x**-2) == "x**(-2)"
    assert str(x**2) == "x**2"
    assert str((x + y)**-1) == "1/(x + y)"
    assert str((x + y)**-2) == "(x + y)**(-2)"
    assert str((x + y)**2) == "(x + y)**2"
    assert str((x + y)**(1 + x)) == "(x + y)**(x + 1)"
    assert str(x**Rational(1, 3)) == "x**(1/3)"
    assert str(1/x**Rational(1, 3)) == "x**(-1/3)"
    assert str(sqrt(sqrt(x))) == "x**(1/4)"
    # not the same as x**-1
    assert str(x**-1.0) == 'x**(-1.0)'
    # see issue #2860
    assert str(Pow(S(2), -1.0, evaluate=False)) == '2**(-1.0)'

