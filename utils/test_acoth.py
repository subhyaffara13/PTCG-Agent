
def test_acoth():
    x = Symbol('x')

    #at specific points
    assert acoth(0) == I*pi/2
    assert acoth(I) == -I*pi/4
    assert acoth(-I) == I*pi/4
    assert acoth(1) is oo
    assert acoth(-1) is -oo
    assert acoth(nan) is nan

    # at infinites
    assert acoth(oo) == 0
    assert acoth(-oo) == 0
    assert acoth(I*oo) == 0
    assert acoth(-I*oo) == 0
    assert acoth(zoo) == 0

    #properties
    assert acoth(-x) == -acoth(x)

    assert acoth(I/sqrt(3)) == -I*pi/3
    assert acoth(-I/sqrt(3)) == I*pi/3
    assert acoth(I*sqrt(3)) == -I*pi/6
    assert acoth(-I*sqrt(3)) == I*pi/6
    assert acoth(I*(1 + sqrt(2))) == -pi*I/8
    assert acoth(-I*(sqrt(2) + 1)) == pi*I/8
    assert acoth(I*(1 - sqrt(2))) == pi*I*Rational(3, 8)
    assert acoth(I*(sqrt(2) - 1)) == pi*I*Rational(-3, 8)
    assert acoth(I*sqrt(5 + 2*sqrt(5))) == -I*pi/10
    assert acoth(-I*sqrt(5 + 2*sqrt(5))) == I*pi/10
    assert acoth(I*(2 + sqrt(3))) == -pi*I/12
    assert acoth(-I*(2 + sqrt(3))) == pi*I/12
    assert acoth(I*(2 - sqrt(3))) == pi*I*Rational(-5, 12)
    assert acoth(I*(sqrt(3) - 2)) == pi*I*Rational(5, 12)

    # reality
    assert acoth(S(2)).is_real is True
    assert acoth(S(2)).is_finite is True
    assert acoth(S(2)).is_extended_real is True
    assert acoth(S(-2)).is_real is True
    assert acoth(S(1)).is_real is False
    assert acoth(S(1)).is_extended_real is True
    assert acoth(S(-1)).is_real is False
    assert acoth(symbols('y', real=True)).is_real is None

    # Symmetry
    assert acoth(Rational(-1, 2)) == -acoth(S.Half)

