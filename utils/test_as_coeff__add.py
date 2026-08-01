
def test_as_coeff_Add():
    assert Integer(3).as_coeff_Add() == (Integer(3), Integer(0))
    assert Rational(3, 4).as_coeff_Add() == (Rational(3, 4), Integer(0))
    assert Float(5.0).as_coeff_Add() == (Float(5.0), Integer(0))

    assert (Integer(3) + x).as_coeff_Add() == (Integer(3), x)
    assert (Rational(3, 4) + x).as_coeff_Add() == (Rational(3, 4), x)
    assert (Float(5.0) + x).as_coeff_Add() == (Float(5.0), x)
    assert (Float(5.0) + x).as_coeff_Add(rational=True) == (0, Float(5.0) + x)

    assert (Integer(3) + x + y).as_coeff_Add() == (Integer(3), x + y)
    assert (Rational(3, 4) + x + y).as_coeff_Add() == (Rational(3, 4), x + y)
    assert (Float(5.0) + x + y).as_coeff_Add() == (Float(5.0), x + y)

    assert (x).as_coeff_Add() == (S.Zero, x)
    assert (x*y).as_coeff_Add() == (S.Zero, x*y)

