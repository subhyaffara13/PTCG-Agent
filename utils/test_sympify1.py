
def test_sympify1():
    assert sympify("x") == Symbol("x")
    assert sympify("   x") == Symbol("x")
    assert sympify("   x   ") == Symbol("x")
    # issue 4877
    assert sympify('--.5') == 0.5
    assert sympify('-1/2') == -S.Half
    assert sympify('-+--.5') == -0.5
    assert sympify('-.[3]') == Rational(-1, 3)
    assert sympify('.[3]') == Rational(1, 3)
    assert sympify('+.[3]') == Rational(1, 3)
    assert sympify('+0.[3]*10**-2') == Rational(1, 300)
    assert sympify('.[052631578947368421]') == Rational(1, 19)
    assert sympify('.0[526315789473684210]') == Rational(1, 19)
    assert sympify('.034[56]') == Rational(1711, 49500)
    # options to make reals into rationals
    assert sympify('1.22[345]', rational=True) == \
        1 + Rational(22, 100) + Rational(345, 99900)
    assert sympify('2/2.6', rational=True) == Rational(10, 13)
    assert sympify('2.6/2', rational=True) == Rational(13, 10)
    assert sympify('2.6e2/17', rational=True) == Rational(260, 17)
    assert sympify('2.6e+2/17', rational=True) == Rational(260, 17)
    assert sympify('2.6e-2/17', rational=True) == Rational(26, 17000)
    assert sympify('2.1+3/4', rational=True) == \
        Rational(21, 10) + Rational(3, 4)
    assert sympify('2.234456', rational=True) == Rational(279307, 125000)
    assert sympify('2.234456e23', rational=True) == 223445600000000000000000
    assert sympify('2.234456e-23', rational=True) == \
        Rational(279307, 12500000000000000000000000000)
    assert sympify('-2.234456e-23', rational=True) == \
        Rational(-279307, 12500000000000000000000000000)
    assert sympify('12345678901/17', rational=True) == \
        Rational(12345678901, 17)
    assert sympify('1/.3 + x', rational=True) == Rational(10, 3) + x
    # make sure longs in fractions work
    assert sympify('222222222222/11111111111') == \
        Rational(222222222222, 11111111111)
    # ... even if they come from repetend notation
    assert sympify('1/.2[123456789012]') == Rational(333333333333, 70781892967)
    # ... or from high precision reals
    assert sympify('.1234567890123456', rational=True) == \
        Rational(19290123283179, 156250000000000)

