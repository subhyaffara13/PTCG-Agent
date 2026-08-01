
def test_as_coeff_Mul():
    assert Integer(3).as_coeff_Mul() == (Integer(3), Integer(1))
    assert Rational(3, 4).as_coeff_Mul() == (Rational(3, 4), Integer(1))
    assert Float(5.0).as_coeff_Mul() == (Float(5.0), Integer(1))
    assert Float(0.0).as_coeff_Mul() == (Float(0.0), Integer(1))

    assert (Integer(3)*x).as_coeff_Mul() == (Integer(3), x)
    assert (Rational(3, 4)*x).as_coeff_Mul() == (Rational(3, 4), x)
    assert (Float(5.0)*x).as_coeff_Mul() == (Float(5.0), x)

    assert (Integer(3)*x*y).as_coeff_Mul() == (Integer(3), x*y)
    assert (Rational(3, 4)*x*y).as_coeff_Mul() == (Rational(3, 4), x*y)
    assert (Float(5.0)*x*y).as_coeff_Mul() == (Float(5.0), x*y)

    assert (x).as_coeff_Mul() == (S.One, x)
    assert (x*y).as_coeff_Mul() == (S.One, x*y)
    assert (-oo*x).as_coeff_Mul(rational=True) == (-1, oo*x)

