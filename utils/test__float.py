
def test_Float():
    sT(Float('1.23', dps=3), "Float('1.22998', precision=13)")
    sT(Float('1.23456789', dps=9), "Float('1.23456788994', precision=33)")
    sT(Float('1.234567890123456789', dps=19),
       "Float('1.234567890123456789013', precision=66)")
    sT(Float('0.60038617995049726', dps=15),
       "Float('0.60038617995049726', precision=53)")

    sT(Float('1.23', precision=13), "Float('1.22998', precision=13)")
    sT(Float('1.23456789', precision=33),
       "Float('1.23456788994', precision=33)")
    sT(Float('1.234567890123456789', precision=66),
       "Float('1.234567890123456789013', precision=66)")
    sT(Float('0.60038617995049726', precision=53),
       "Float('0.60038617995049726', precision=53)")

    sT(Float('0.60038617995049726', 15),
       "Float('0.60038617995049726', precision=53)")


def test_Float():
    assert smtlib_code(0.0) == "0.0"
    assert smtlib_code(0.000000000000000003) == '(* 3.0 (pow 10 -18))'
    assert smtlib_code(5.3) == "5.3"


def test_Float():
    # NOTE dps is the whole number of decimal digits
    assert str(Float('1.23', dps=1 + 2)) == '1.23'
    assert str(Float('1.23456789', dps=1 + 8)) == '1.23456789'
    assert str(
        Float('1.234567890123456789', dps=1 + 18)) == '1.234567890123456789'
    assert str(pi.evalf(1 + 2)) == '3.14'
    assert str(pi.evalf(1 + 14)) == '3.14159265358979'
    assert str(pi.evalf(1 + 64)) == ('3.141592653589793238462643383279'
                                     '5028841971693993751058209749445923')
    assert str(pi.round(-1)) == '0.0'
    assert str((pi**400 - (pi**400).round(1)).n(2)) == '-0.e+88'
    assert sstr(Float("100"), full_prec=False, min=-2, max=2) == '1.0e+2'
    assert sstr(Float("100"), full_prec=False, min=-2, max=3) == '100.0'
    assert sstr(Float("0.1"), full_prec=False, min=-2, max=3) == '0.1'
    assert sstr(Float("0.099"), min=-2, max=3) == '9.90000000000000e-2'


def test_Float():
    def eq(a, b):
        t = Float("1.0E-15")
        return (-t < a - b < t)

    equal_pairs = [
        (0, 0.0), # This is just how Python works...
        (0, S.Zero),
        (0.0, Float(0)),
    ]
    unequal_pairs = [
        (0.0, S.Zero),
        (0, Float(0)),
        (S.Zero, Float(0)),
    ]
    for p1, p2 in equal_pairs:
        assert (p1 == p2) is True
        assert (p1 != p2) is False
        assert (p2 == p1) is True
        assert (p2 != p1) is False
    for p1, p2 in unequal_pairs:
        assert (p1 == p2) is False
        assert (p1 != p2) is True
        assert (p2 == p1) is False
        assert (p2 != p1) is True

    assert S.Zero.is_zero

    a = Float(2) ** Float(3)
    assert eq(a.evalf(), Float(8))
    assert eq((pi ** -1).evalf(), Float("0.31830988618379067"))
    a = Float(2) ** Float(4)
    assert eq(a.evalf(), Float(16))
    assert (S(.3) == S(.5)) is False

    mpf = (0, 5404319552844595, -52, 53)
    x_str = Float((0, '13333333333333', -52, 53))
    x_0xstr = Float((0, '0x13333333333333', -52, 53))
    x2_str = Float((0, '26666666666666', -53, 54))
    x_hex = Float((0, int(0x13333333333333), -52, 53))
    x_dec = Float(mpf)
    assert x_str == x_0xstr == x_hex == x_dec == Float(1.2)
    # x2_str was entered slightly malformed in that the mantissa
    # was even -- it should be odd and the even part should be
    # included with the exponent, but this is resolved by normalization
    # ONLY IF REQUIREMENTS of mpf_norm are met: the bitcount must
    # be exact: double the mantissa ==> increase bc by 1
    assert Float(1.2)._mpf_ == mpf
    assert x2_str._mpf_ == mpf

    assert Float((0, int(0), -123, -1)) is S.NaN
    assert Float((0, int(0), -456, -2)) is S.Infinity
    assert Float((1, int(0), -789, -3)) is S.NegativeInfinity
    # if you don't give the full signature, it's not special
    assert Float((0, int(0), -123)) == Float(0)
    assert Float((0, int(0), -456)) == Float(0)
    assert Float((1, int(0), -789)) == Float(0)

    raises(ValueError, lambda: Float((0, 7, 1, 3), ''))

    assert Float('0.0').is_finite is True
    assert Float('0.0').is_negative is False
    assert Float('0.0').is_positive is False
    assert Float('0.0').is_infinite is False
    assert Float('0.0').is_zero is True

    # rationality properties
    # if the integer test fails then the use of intlike
    # should be removed from gamma_functions.py
    assert Float(1).is_integer is None
    assert Float(1).is_rational is None
    assert Float(1).is_irrational is None
    assert sqrt(2).n(15).is_rational is None
    assert sqrt(2).n(15).is_irrational is None

    # do not automatically evalf
    def teq(a):
        assert (a.evalf() == a) is False
        assert (a.evalf() != a) is True
        assert (a == a.evalf()) is False
        assert (a != a.evalf()) is True

    teq(pi)
    teq(2*pi)
    teq(cos(0.1, evaluate=False))

    # long integer
    i = 12345678901234567890
    assert same_and_same_prec(Float(12, ''), Float('12', ''))
    assert same_and_same_prec(Float(Integer(i), ''), Float(i, ''))
    assert same_and_same_prec(Float(i, ''), Float(str(i), 20))
    assert same_and_same_prec(Float(str(i)), Float(i, ''))
    assert same_and_same_prec(Float(i), Float(i, ''))

    # inexact floats (repeating binary = denom not multiple of 2)
    # cannot have precision greater than 15
    assert Float(.125, 22)._prec == 76
    assert Float(2.0, 22)._prec == 76
    # only default prec is equal, even for exactly representable float
    assert Float(.125, 22) != .125
    #assert Float(2.0, 22) == 2
    assert float(Float('.12500000000000001', '')) == .125
    raises(ValueError, lambda: Float(.12500000000000001, ''))

    # allow spaces
    assert Float('123 456.123 456') == Float('123456.123456')
    assert Integer('123 456') == Integer('123456')
    assert Rational('123 456.123 456') == Rational('123456.123456')
    assert Float(' .3e2') == Float('0.3e2')
    # but treat them as strictly ass underscore between digits: only 1
    raises(ValueError, lambda: Float('1  2'))

    # allow underscore between digits
    assert Float('1_23.4_56') == Float('123.456')
    # assert Float('1_23.4_5_6', 12) == Float('123.456', 12)
    # ...but not in all cases (per Py 3.6)
    raises(ValueError, lambda: Float('1_'))
    raises(ValueError, lambda: Float('1__2'))
    raises(ValueError, lambda: Float('_1'))
    raises(ValueError, lambda: Float('_inf'))

    # allow auto precision detection
    assert Float('.1', '') == Float(.1, 1)
    assert Float('.125', '') == Float(.125, 3)
    assert Float('.100', '') == Float(.1, 3)
    assert Float('2.0', '') == Float('2', 2)

    raises(ValueError, lambda: Float("12.3d-4", ""))
    raises(ValueError, lambda: Float(12.3, ""))
    raises(ValueError, lambda: Float('.'))
    raises(ValueError, lambda: Float('-.'))

    zero = Float('0.0')
    assert Float('-0') == zero
    assert Float('.0') == zero
    assert Float('-.0') == zero
    assert Float('-0.0') == zero
    assert Float(0.0) == zero
    assert Float(0) == zero
    assert Float(0, '') == Float('0', '')
    assert Float(1) == Float(1.0)
    assert Float(S.Zero) == zero
    assert Float(S.One) == Float(1.0)

    assert Float(decimal.Decimal('0.1'), 3) == Float('.1', 3)
    assert Float(decimal.Decimal('nan')) is S.NaN
    assert Float(decimal.Decimal('Infinity')) is S.Infinity
    assert Float(decimal.Decimal('-Infinity')) is S.NegativeInfinity

    assert '{:.3f}'.format(Float(4.236622)) == '4.237'
    assert '{:.35f}'.format(Float(pi.n(40), 40)) == \
        '3.14159265358979323846264338327950288'

    # unicode
    assert Float('0.73908513321516064100000000') == \
        Float('0.73908513321516064100000000')
    assert Float('0.73908513321516064100000000', 28) == \
        Float('0.73908513321516064100000000', 28)

    # binary precision
    # Decimal value 0.1 cannot be expressed precisely as a base 2 fraction
    a = Float(S.One/10, dps=15)
    b = Float(S.One/10, dps=16)
    p = Float(S.One/10, precision=53)
    q = Float(S.One/10, precision=54)
    assert a._mpf_ == p._mpf_
    assert not a._mpf_ == q._mpf_
    assert not b._mpf_ == q._mpf_

    # Precision specifying errors
    raises(ValueError, lambda: Float("1.23", dps=3, precision=10))
    raises(ValueError, lambda: Float("1.23", dps="", precision=10))
    raises(ValueError, lambda: Float("1.23", dps=3, precision=""))
    raises(ValueError, lambda: Float("1.23", dps="", precision=""))

    # from NumberSymbol
    assert same_and_same_prec(Float(pi, 32), pi.evalf(32))
    assert same_and_same_prec(Float(Catalan), Catalan.evalf())

    # oo and nan
    u = ['inf', '-inf', 'nan', 'iNF', '+inf']
    v = [oo, -oo, nan, oo, oo]
    for i, a in zip(u, v):
        assert Float(i) is a

