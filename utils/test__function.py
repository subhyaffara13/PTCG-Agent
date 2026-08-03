from typing import Callable

def test_Function():
    assert julia_code(sin(x) ** cos(x)) == "sin(x) .^ cos(x)"
    assert julia_code(abs(x)) == "abs(x)"
    assert julia_code(ceiling(x)) == "ceil(x)"


def test_Function():
    assert maple_code(sin(x) ** cos(x)) == "sin(x)^cos(x)"
    assert maple_code(abs(x)) == "abs(x)"
    assert maple_code(ceiling(x)) == "ceil(x)"


def test_Function():
    assert mcode(f(x, y, z)) == "f[x, y, z]"
    assert mcode(sin(x) ** cos(x)) == "Sin[x]^Cos[x]"
    assert mcode(sec(x) * acsc(x)) == "ArcCsc[x]*Sec[x]"
    assert mcode(atan2(y, x)) == "ArcTan[x, y]"
    assert mcode(conjugate(x)) == "Conjugate[x]"
    assert mcode(Max(x, y, z)*Min(y, z)) == "Max[x, y, z]*Min[y, z]"
    assert mcode(fresnelc(x)) == "FresnelC[x]"
    assert mcode(fresnels(x)) == "FresnelS[x]"
    assert mcode(gamma(x)) == "Gamma[x]"
    assert mcode(uppergamma(x, y)) == "Gamma[x, y]"
    assert mcode(polygamma(x, y)) == "PolyGamma[x, y]"
    assert mcode(loggamma(x)) == "LogGamma[x]"
    assert mcode(erf(x)) == "Erf[x]"
    assert mcode(erfc(x)) == "Erfc[x]"
    assert mcode(erfi(x)) == "Erfi[x]"
    assert mcode(erf2(x, y)) == "Erf[x, y]"
    assert mcode(expint(x, y)) == "ExpIntegralE[x, y]"
    assert mcode(erfcinv(x)) == "InverseErfc[x]"
    assert mcode(erfinv(x)) == "InverseErf[x]"
    assert mcode(erf2inv(x, y)) == "InverseErf[x, y]"
    assert mcode(Ei(x)) == "ExpIntegralEi[x]"
    assert mcode(Ci(x)) == "CosIntegral[x]"
    assert mcode(li(x)) == "LogIntegral[x]"
    assert mcode(Si(x)) == "SinIntegral[x]"
    assert mcode(Shi(x)) == "SinhIntegral[x]"
    assert mcode(Chi(x)) == "CoshIntegral[x]"
    assert mcode(beta(x, y)) == "Beta[x, y]"
    assert mcode(factorial(x)) == "Factorial[x]"
    assert mcode(factorial2(x)) == "Factorial2[x]"
    assert mcode(subfactorial(x)) == "Subfactorial[x]"
    assert mcode(FallingFactorial(x, y)) == "FactorialPower[x, y]"
    assert mcode(RisingFactorial(x, y)) == "Pochhammer[x, y]"
    assert mcode(catalan(x)) == "CatalanNumber[x]"
    assert mcode(harmonic(x)) == "HarmonicNumber[x]"
    assert mcode(harmonic(x, y)) == "HarmonicNumber[x, y]"
    assert mcode(Li(x)) == "LogIntegral[x] - LogIntegral[2]"
    assert mcode(LambertW(x)) == "ProductLog[x]"
    assert mcode(LambertW(x, -1)) == "ProductLog[-1, x]"
    assert mcode(LambertW(x, y)) == "ProductLog[y, x]"


def test_Function():
    assert mcode(sin(x) ** cos(x)) == "sin(x).^cos(x)"
    assert mcode(sign(x)) == "sign(x)"
    assert mcode(exp(x)) == "exp(x)"
    assert mcode(log(x)) == "log(x)"
    assert mcode(factorial(x)) == "factorial(x)"
    assert mcode(floor(x)) == "floor(x)"
    assert mcode(atan2(y, x)) == "atan2(y, x)"
    assert mcode(beta(x, y)) == 'beta(x, y)'
    assert mcode(polylog(x, y)) == 'polylog(x, y)'
    assert mcode(harmonic(x)) == 'harmonic(x)'
    assert mcode(bernoulli(x)) == "bernoulli(x)"
    assert mcode(bernoulli(x, y)) == "bernoulli(x, y)"
    assert mcode(legendre(x, y)) == "legendre(x, y)"


def test_Function():
    assert precedence(sin(x)) == PRECEDENCE["Func"]


def test_Function():
    sT(Function("f")(x), "Function('f')(Symbol('x'))")
    # test unapplied Function
    sT(Function('f'), "Function('f')")

    sT(sin(x), "sin(Symbol('x'))")
    sT(sin, "sin")


def test_Function():
    with _check_warns([_W.DEFAULTING_TO_FLOAT, _W.WILL_NOT_ASSERT]) as w:
        assert smtlib_code(sin(x) ** cos(x), auto_declare=False, log_warn=w) == "(pow (sin x) (cos x))"

    with _check_warns([_W.WILL_NOT_ASSERT]) as w:
        assert smtlib_code(
            abs(x),
            symbol_table={x: int, y: bool},
            known_types={int: "INTEGER_TYPE"},
            known_functions={sympy.Abs: "ABSOLUTE_VALUE_OF"},
            log_warn=w
        ) == "(declare-const x INTEGER_TYPE)\n" \
             "(ABSOLUTE_VALUE_OF x)"

    my_fun1 = Function('f1')
    with _check_warns([_W.WILL_NOT_ASSERT]) as w:
        assert smtlib_code(
            my_fun1(x),
            symbol_table={my_fun1: Callable[[bool], float]},
            log_warn=w
        ) == "(declare-const x Bool)\n" \
             "(declare-fun f1 (Bool) Real)\n" \
             "(f1 x)"

    with _check_warns([]) as w:
        assert smtlib_code(
            my_fun1(x),
            symbol_table={my_fun1: Callable[[bool], bool]},
            log_warn=w
        ) == "(declare-const x Bool)\n" \
             "(declare-fun f1 (Bool) Bool)\n" \
             "(assert (f1 x))"

        assert smtlib_code(
            Eq(my_fun1(x, z), y),
            symbol_table={my_fun1: Callable[[int, bool], bool]},
            log_warn=w
        ) == "(declare-const x Int)\n" \
             "(declare-const y Bool)\n" \
             "(declare-const z Bool)\n" \
             "(declare-fun f1 (Int Bool) Bool)\n" \
             "(assert (= (f1 x z) y))"

        assert smtlib_code(
            Eq(my_fun1(x, z), y),
            symbol_table={my_fun1: Callable[[int, bool], bool]},
            known_functions={my_fun1: "MY_KNOWN_FUN", Eq: '=='},
            log_warn=w
        ) == "(declare-const x Int)\n" \
             "(declare-const y Bool)\n" \
             "(declare-const z Bool)\n" \
             "(assert (== (MY_KNOWN_FUN x z) y))"

    with _check_warns([_W.DEFAULTING_TO_FLOAT] * 3) as w:
        assert smtlib_code(
            Eq(my_fun1(x, z), y),
            known_functions={my_fun1: "MY_KNOWN_FUN", Eq: '=='},
            log_warn=w
        ) == "(declare-const x Real)\n" \
             "(declare-const y Real)\n" \
             "(declare-const z Real)\n" \
             "(assert (== (MY_KNOWN_FUN x z) y))"


def test_Function():
    f = Function('f')
    fx = f(x)
    w = WildFunction('w')
    assert str(f) == "f"
    assert str(fx) == "f(x)"
    assert str(w) == "w_"


def test_Function():
    class myfunc(Function):
        @classmethod
        def eval(cls):  # zero args
            return

    assert myfunc.nargs == FiniteSet(0)
    assert myfunc().nargs == FiniteSet(0)
    raises(TypeError, lambda: myfunc(x).nargs)

    class myfunc(Function):
        @classmethod
        def eval(cls, x):  # one arg
            return

    assert myfunc.nargs == FiniteSet(1)
    assert myfunc(x).nargs == FiniteSet(1)
    raises(TypeError, lambda: myfunc(x, y).nargs)

    class myfunc(Function):
        @classmethod
        def eval(cls, *x):  # star args
            return

    assert myfunc.nargs == S.Naturals0
    assert myfunc(x).nargs == S.Naturals0

