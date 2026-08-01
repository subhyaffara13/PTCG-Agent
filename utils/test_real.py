
def test_real():
    x = Normal('x', 0, 1)
    assert x.is_real


def test_real():
    x = Symbol('x', real=True)

    I = Interval(0, 5)
    J = Interval(10, 20)
    A = FiniteSet(1, 2, 30, x, S.Pi)
    B = FiniteSet(-4, 0)
    C = FiniteSet(100)
    D = FiniteSet('Ham', 'Eggs')

    assert all(s.is_subset(S.Reals) for s in [I, J, A, B, C])
    assert not D.is_subset(S.Reals)
    assert all((a + b).is_subset(S.Reals) for a in [I, J, A, B, C] for b in [I, J, A, B, C])
    assert not any((a + D).is_subset(S.Reals) for a in [I, J, A, B, C, D])

    assert not (I + A + D).is_subset(S.Reals)


def test_real():
    assert satask(Q.real(x*y), Q.real(x) & Q.real(y)) is True
    assert satask(Q.real(x + y), Q.real(x) & Q.real(y)) is True
    assert satask(Q.real(x*y*z), Q.real(x) & Q.real(y) & Q.real(z)) is True
    assert satask(Q.real(x*y*z), Q.real(x) & Q.real(y)) is None
    assert satask(Q.real(x*y*z), Q.real(x) & Q.real(y) & Q.imaginary(z)) is False
    assert satask(Q.real(x + y + z), Q.real(x) & Q.real(y) & Q.real(z)) is True
    assert satask(Q.real(x + y + z), Q.real(x) & Q.real(y)) is None

