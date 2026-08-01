
def test_1_over_x_and_sqrt():
    # 1.0 and 0.5 would do something different in regular StrPrinter,
    # but these are exact in IEEE floating point so no different here.
    assert julia_code(1/x) == '1 ./ x'
    assert julia_code(x**-1) == julia_code(x**-1.0) == '1 ./ x'
    assert julia_code(1/sqrt(x)) == '1 ./ sqrt(x)'
    assert julia_code(x**-S.Half) == julia_code(x**-0.5) == '1 ./ sqrt(x)'
    assert julia_code(sqrt(x)) == 'sqrt(x)'
    assert julia_code(x**S.Half) == julia_code(x**0.5) == 'sqrt(x)'
    assert julia_code(1/pi) == '1 / pi'
    assert julia_code(pi**-1) == julia_code(pi**-1.0) == '1 / pi'
    assert julia_code(pi**-0.5) == '1 / sqrt(pi)'


def test_1_over_x_and_sqrt():
    # 1.0 and 0.5 would do something different in regular StrPrinter,
    # but these are exact in IEEE floating point so no different here.
    assert maple_code(1 / x) == '1/x'
    assert maple_code(x ** -1) == maple_code(x ** -1.0) == '1/x'
    assert maple_code(1 / sqrt(x)) == '1/sqrt(x)'
    assert maple_code(x ** -S.Half) == maple_code(x ** -0.5) == '1/sqrt(x)'
    assert maple_code(sqrt(x)) == 'sqrt(x)'
    assert maple_code(x ** S.Half) == maple_code(x ** 0.5) == 'sqrt(x)'
    assert maple_code(1 / pi) == '1/Pi'
    assert maple_code(pi ** -1) == maple_code(pi ** -1.0) == '1/Pi'
    assert maple_code(pi ** -0.5) == '1/sqrt(Pi)'


def test_1_over_x_and_sqrt():
    # 1.0 and 0.5 would do something different in regular StrPrinter,
    # but these are exact in IEEE floating point so no different here.
    assert mcode(1/x) == '1./x'
    assert mcode(x**-1) == mcode(x**-1.0) == '1./x'
    assert mcode(1/sqrt(x)) == '1./sqrt(x)'
    assert mcode(x**-S.Half) == mcode(x**-0.5) == '1./sqrt(x)'
    assert mcode(sqrt(x)) == 'sqrt(x)'
    assert mcode(x**S.Half) == mcode(x**0.5) == 'sqrt(x)'
    assert mcode(1/pi) == '1/pi'
    assert mcode(pi**-1) == mcode(pi**-1.0) == '1/pi'
    assert mcode(pi**-0.5) == '1/sqrt(pi)'

