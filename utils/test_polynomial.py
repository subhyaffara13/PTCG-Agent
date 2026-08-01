
def test_polynomial():
    from sympy.core.numbers import oo
    assert hyperexpand(hyper([], [-1], z)) is oo
    assert hyperexpand(hyper([-2], [-1], z)) is oo
    assert hyperexpand(hyper([0, 0], [-1], z)) == 1
    assert can_do([-5, -2, randcplx(), randcplx()], [-10, randcplx()])
    assert hyperexpand(hyper((-1, 1), (-2,), z)) == 1 + z/2


def test_polynomial():
    assert limit((x + 1)**1000/((x + 1)**1000 + 1), x, oo) == 1
    assert limit((x + 1)**1000/((x + 1)**1000 + 1), x, -oo) == 1
    assert limit(x ** Rational(77, 3) / (1 + x ** Rational(77, 3)), x, oo) == 1
    assert limit(x ** 101.1 / (1 + x ** 101.1), x, oo) == 1

