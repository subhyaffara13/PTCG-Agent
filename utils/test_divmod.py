import random
import re
from typing import Tuple

def test_divmod():
    assert divmod(x, y) == (x//y, x % y)
    assert divmod(x, 3) == (x//3, x % 3)
    assert divmod(3, x) == (3//x, 3 % x)


def test_divmod():
    x = Symbol("x")
    assert divmod(S(12), S(8)) == Tuple(1, 4)
    assert divmod(-S(12), S(8)) == Tuple(-2, 4)
    assert divmod(S.Zero, S.One) == Tuple(0, 0)
    raises(ZeroDivisionError, lambda: divmod(S.Zero, S.Zero))
    raises(ZeroDivisionError, lambda: divmod(S.One, S.Zero))
    assert divmod(S(12), 8) == Tuple(1, 4)
    assert divmod(12, S(8)) == Tuple(1, 4)
    assert S(1024)//x == 1024//x == floor(1024/x)

    assert divmod(S("2"), S("3/2")) == Tuple(S("1"), S("1/2"))
    assert divmod(S("3/2"), S("2")) == Tuple(S("0"), S("3/2"))
    assert divmod(S("2"), S("3.5")) == Tuple(S("0"), S("2."))
    assert divmod(S("3.5"), S("2")) == Tuple(S("1"), S("1.5"))
    assert divmod(S("2"), S("1/3")) == Tuple(S("6"), S("0"))
    assert divmod(S("1/3"), S("2")) == Tuple(S("0"), S("1/3"))
    assert divmod(S("2"), S("1/10")) == Tuple(S("20"), S("0"))
    assert divmod(S("2"), S(".1"))[0] == 19
    assert divmod(S("0.1"), S("2")) == Tuple(S("0"), S("0.1"))
    assert divmod(S("2"), 2) == Tuple(S("1"), S("0"))
    assert divmod(2, S("2")) == Tuple(S("1"), S("0"))
    assert divmod(S("2"), 1.5) == Tuple(S("1"), S("0.5"))
    assert divmod(1.5, S("2")) == Tuple(S("0"), S("1.5"))
    assert divmod(0.3, S("2")) == Tuple(S("0"), S("0.3"))
    assert divmod(S("3/2"), S("3.5")) == Tuple(S("0"), S(3/2))
    assert divmod(S("3.5"), S("3/2")) == Tuple(S("2"), S("0.5"))
    assert divmod(S("3/2"), S("1/3")) == Tuple(S("4"), S("1/6"))
    assert divmod(S("1/3"), S("3/2")) == Tuple(S("0"), S("1/3"))
    assert divmod(S("3/2"), S("0.1"))[0] == 14
    assert divmod(S("0.1"), S("3/2")) == Tuple(S("0"), S("0.1"))
    assert divmod(S("3/2"), 2) == Tuple(S("0"), S("3/2"))
    assert divmod(2, S("3/2")) == Tuple(S("1"), S("1/2"))
    assert divmod(S("3/2"), 1.5) == Tuple(S("1"), S("0."))
    assert divmod(1.5, S("3/2")) == Tuple(S("1"), S("0."))
    assert divmod(S("3/2"), 0.3) == Tuple(S("5"), S("0."))
    assert divmod(0.3, S("3/2")) == Tuple(S("0"), S("0.3"))
    assert divmod(S("1/3"), S("3.5")) == (0, 1/3)
    assert divmod(S("3.5"), S("0.1")) == Tuple(S("35"), S("0."))
    assert divmod(S("0.1"), S("3.5")) == Tuple(S("0"), S("0.1"))
    assert divmod(S("3.5"), 2) == Tuple(S("1"), S("1.5"))
    assert divmod(2, S("3.5")) == Tuple(S("0"), S("2."))
    assert divmod(S("3.5"), 1.5) == Tuple(S("2"), S("0.5"))
    assert divmod(1.5, S("3.5")) == Tuple(S("0"), S("1.5"))
    assert divmod(0.3, S("3.5")) == Tuple(S("0"), S("0.3"))
    assert divmod(S("0.1"), S("1/3")) == Tuple(S("0"), S("0.1"))
    assert divmod(S("1/3"), 2) == Tuple(S("0"), S("1/3"))
    assert divmod(2, S("1/3")) == Tuple(S("6"), S("0"))
    assert divmod(S("1/3"), 1.5) == (0, 1/3)
    assert divmod(0.3, S("1/3")) == (0, 0.3)
    assert divmod(S("0.1"), 2) == (0, 0.1)
    assert divmod(2, S("0.1"))[0] == 19
    assert divmod(S("0.1"), 1.5) == (0, 0.1)
    assert divmod(1.5, S("0.1")) == Tuple(S("15"), S("0."))
    assert divmod(S("0.1"), 0.3) == Tuple(S("0"), S("0.1"))

    assert str(divmod(S("2"), 0.3)) == '(6, 0.2)'
    assert str(divmod(S("3.5"), S("1/3"))) == '(10, 0.166666666666667)'
    assert str(divmod(S("3.5"), 0.3)) == '(11, 0.2)'
    assert str(divmod(S("1/3"), S("0.1"))) == '(3, 0.0333333333333333)'
    assert str(divmod(1.5, S("1/3"))) == '(4, 0.166666666666667)'
    assert str(divmod(S("1/3"), 0.3)) == '(1, 0.0333333333333333)'
    assert str(divmod(0.3, S("0.1"))) == '(2, 0.1)'

    assert divmod(-3, S(2)) == (-2, 1)
    assert divmod(S(-3), S(2)) == (-2, 1)
    assert divmod(S(-3), 2) == (-2, 1)

    assert divmod(oo, 1) == (S.NaN, S.NaN)
    assert divmod(S.NaN, 1) == (S.NaN, S.NaN)
    assert divmod(1, S.NaN) == (S.NaN, S.NaN)
    ans = [(-1, oo), (-1, oo), (0, 0), (0, 1), (0, 2)]
    OO = float('inf')
    ANS = [tuple(map(float, i)) for i in ans]
    assert [divmod(i, oo) for i in range(-2, 3)] == ans
    ans = [(0, -2), (0, -1), (0, 0), (-1, -oo), (-1, -oo)]
    ANS = [tuple(map(float, i)) for i in ans]
    assert [divmod(i, -oo) for i in range(-2, 3)] == ans
    assert [divmod(i, -OO) for i in range(-2, 3)] == ANS

    # sympy's divmod gives an Integer for the quotient rather than a float
    dmod = lambda a, b: tuple([j if i else int(j) for i, j in enumerate(divmod(a, b))])
    for a in (4, 4., 4.25, 0, 0., -4, -4. -4.25):
        for b in (2, 2., 2.5, -2, -2., -2.5):
            assert divmod(S(a), S(b)) == dmod(a, b)


def test_divmod():
    msg = re.escape("unsupported operand type(s) for divmod(): 'Expression' and 'int'")
    with pytest.raises(TypeError, match=msg):
        divmod(pd.col("a"), 2)


def test_divmod(Poly):
    # This checks commutation, not numerical correctness
    c1 = list(random((4,)) + .5)
    c2 = list(random((3,)) + .5)
    c3 = list(random((2,)) + .5)
    p1 = Poly(c1)
    p2 = Poly(c2)
    p3 = Poly(c3)
    p4 = p1 * p2 + p3
    c4 = list(p4.coef)
    quo, rem = divmod(p4, p2)
    assert_poly_almost_equal(quo, p1)
    assert_poly_almost_equal(rem, p3)
    quo, rem = divmod(p4, c2)
    assert_poly_almost_equal(quo, p1)
    assert_poly_almost_equal(rem, p3)
    quo, rem = divmod(c4, p2)
    assert_poly_almost_equal(quo, p1)
    assert_poly_almost_equal(rem, p3)
    quo, rem = divmod(p4, tuple(c2))
    assert_poly_almost_equal(quo, p1)
    assert_poly_almost_equal(rem, p3)
    quo, rem = divmod(tuple(c4), p2)
    assert_poly_almost_equal(quo, p1)
    assert_poly_almost_equal(rem, p3)
    quo, rem = divmod(p4, np.array(c2))
    assert_poly_almost_equal(quo, p1)
    assert_poly_almost_equal(rem, p3)
    quo, rem = divmod(np.array(c4), p2)
    assert_poly_almost_equal(quo, p1)
    assert_poly_almost_equal(rem, p3)
    quo, rem = divmod(p2, 2)
    assert_poly_almost_equal(quo, 0.5 * p2)
    assert_poly_almost_equal(rem, Poly([0]))
    quo, rem = divmod(2, p2)
    assert_poly_almost_equal(quo, Poly([0]))
    assert_poly_almost_equal(rem, Poly([2]))
    assert_raises(TypeError, divmod, p1, Poly([0], domain=Poly.domain + 1))
    assert_raises(TypeError, divmod, p1, Poly([0], window=Poly.window + 1))
    if Poly is Polynomial:
        assert_raises(TypeError, divmod, p1, Chebyshev([0]))
    else:
        assert_raises(TypeError, divmod, p1, Polynomial([0]))

