
def test_settings():
    raises(TypeError, lambda: fcode(S(4), method="garbage"))


def test_settings():
    from sympy.abc import x
    raises(TypeError, lambda: print_gtk(x, method="garbage"))


def test_settings():
    raises(TypeError, lambda: lambdarepr(sin(x), method="garbage"))


def test_settings():
    raises(TypeError, lambda: latex(x*y, method="garbage"))


def test_settings():
    raises(TypeError, lambda: python(x, method="garbage"))


def test_settings():
    raises(TypeError, lambda: rust_code(sin(x), method="garbage"))


def test_settings():
    raises(TypeError, lambda: sstr(S(4), method="garbage"))


def test_settings():
    raises(TypeError, lambda: pretty(S(4), method="garbage"))

