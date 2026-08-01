
def test_mix_number_pow_symbols():
    assert julia_code(pi**3) == 'pi ^ 3'
    assert julia_code(x**2) == 'x .^ 2'
    assert julia_code(x**(pi**3)) == 'x .^ (pi ^ 3)'
    assert julia_code(x**y) == 'x .^ y'
    assert julia_code(x**(y**z)) == 'x .^ (y .^ z)'
    assert julia_code((x**y)**z) == '(x .^ y) .^ z'


def test_mix_number_pow_symbols():
    assert maple_code(pi ** 3) == 'Pi^3'
    assert maple_code(x ** 2) == 'x^2'

    assert maple_code(x ** (pi ** 3)) == 'x^(Pi^3)'
    assert maple_code(x ** y) == 'x^y'

    assert maple_code(x ** (y ** z)) == 'x^(y^z)'
    assert maple_code((x ** y) ** z) == '(x^y)^z'


def test_mix_number_pow_symbols():
    assert mcode(pi**3) == 'pi^3'
    assert mcode(x**2) == 'x.^2'
    assert mcode(x**(pi**3)) == 'x.^(pi^3)'
    assert mcode(x**y) == 'x.^y'
    assert mcode(x**(y**z)) == 'x.^(y.^z)'
    assert mcode((x**y)**z) == '(x.^y).^z'

