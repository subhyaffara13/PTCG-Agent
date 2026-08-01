
def test_acsch():
    x = Symbol('x')

    assert unchanged(acsch, x)
    assert acsch(-x) == -acsch(x)

    # values at fixed points
    assert acsch(1) == log(1 + sqrt(2))
    assert acsch(-1) == - log(1 + sqrt(2))
    assert acsch(0) is zoo
    assert acsch(2) == log((1+sqrt(5))/2)
    assert acsch(-2) == - log((1+sqrt(5))/2)

    assert acsch(I) == - I*pi/2
    assert acsch(-I) == I*pi/2
    assert acsch(-I*(sqrt(6) + sqrt(2))) == I*pi / 12
    assert acsch(I*(sqrt(2) + sqrt(6))) == -I*pi / 12
    assert acsch(-I*(1 + sqrt(5))) == I*pi / 10
    assert acsch(I*(1 + sqrt(5))) == -I*pi / 10
    assert acsch(-I*2 / sqrt(2 - sqrt(2))) == I*pi / 8
    assert acsch(I*2 / sqrt(2 - sqrt(2))) == -I*pi / 8
    assert acsch(-I*2) == I*pi / 6
    assert acsch(I*2) == -I*pi / 6
    assert acsch(-I*sqrt(2 + 2/sqrt(5))) == I*pi / 5
    assert acsch(I*sqrt(2 + 2/sqrt(5))) == -I*pi / 5
    assert acsch(-I*sqrt(2)) == I*pi / 4
    assert acsch(I*sqrt(2)) == -I*pi / 4
    assert acsch(-I*(sqrt(5)-1)) == 3*I*pi / 10
    assert acsch(I*(sqrt(5)-1)) == -3*I*pi / 10
    assert acsch(-I*2 / sqrt(3)) == I*pi / 3
    assert acsch(I*2 / sqrt(3)) == -I*pi / 3
    assert acsch(-I*2 / sqrt(2 + sqrt(2))) == 3*I*pi / 8
    assert acsch(I*2 / sqrt(2 + sqrt(2))) == -3*I*pi / 8
    assert acsch(-I*sqrt(2 - 2/sqrt(5))) == 2*I*pi / 5
    assert acsch(I*sqrt(2 - 2/sqrt(5))) == -2*I*pi / 5
    assert acsch(-I*(sqrt(6) - sqrt(2))) == 5*I*pi / 12
    assert acsch(I*(sqrt(6) - sqrt(2))) == -5*I*pi / 12
    assert acsch(nan) is nan

    # properties
    # acsch(x) == asinh(1/x)
    assert acsch(-I*sqrt(2)) == asinh(I/sqrt(2))
    assert acsch(-I*2 / sqrt(3)) == asinh(I*sqrt(3) / 2)

    # reality
    assert acsch(S(2)).is_real is True
    assert acsch(S(2)).is_finite is True
    assert acsch(S(-2)).is_real is True
    assert acsch(S(oo)).is_extended_real is True
    assert acsch(-S(oo)).is_real is True
    assert (acsch(2) - oo) == -oo
    assert acsch(symbols('y', extended_real=True)).is_extended_real is True

    # acsch(x) == -I*asin(I/x)
    assert acsch(-I*sqrt(2)) == -I*asin(-1/sqrt(2))
    assert acsch(-I*2 / sqrt(3)) == -I*asin(-sqrt(3)/2)

    # csch(acsch(x)) / x == 1
    assert expand_mul(csch(acsch(-I*(sqrt(6) + sqrt(2)))) / (-I*(sqrt(6) + sqrt(2)))) == 1
    assert expand_mul(csch(acsch(I*(1 + sqrt(5)))) / (I*(1 + sqrt(5)))) == 1
    assert (csch(acsch(I*sqrt(2 - 2/sqrt(5)))) / (I*sqrt(2 - 2/sqrt(5)))).simplify() == 1
    assert (csch(acsch(-I*sqrt(2 - 2/sqrt(5)))) / (-I*sqrt(2 - 2/sqrt(5)))).simplify() == 1

    # numerical evaluation
    assert str(acsch(5*I+1).n(6)) == '0.0391819 - 0.193363*I'
    assert str(acsch(-5*I+1).n(6)) == '0.0391819 + 0.193363*I'

