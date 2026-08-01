
def test_normalized():
    assert Matrix([3, 4]).normalized() == \
        Matrix([Rational(3, 5), Rational(4, 5)])

    # Zero vector trivial cases
    assert Matrix([0, 0, 0]).normalized() == Matrix([0, 0, 0])

    # Machine precision error truncation trivial cases
    m = Matrix([0,0,1.e-100])
    assert m.normalized(
    iszerofunc=lambda x: x.evalf(n=10, chop=True).is_zero
    ) == Matrix([0, 0, 0])


def test_normalized():
    assert Matrix([3, 4]).normalized() == \
        Matrix([Rational(3, 5), Rational(4, 5)])

    # Zero vector trivial cases
    assert Matrix([0, 0, 0]).normalized() == Matrix([0, 0, 0])

    # Machine precision error truncation trivial cases
    m = Matrix([0,0,1.e-100])
    assert m.normalized(
    iszerofunc=lambda x: x.evalf(n=10, chop=True).is_zero
    ) == Matrix([0, 0, 0])

