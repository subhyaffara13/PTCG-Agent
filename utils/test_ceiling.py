
def test_ceiling():
    assert limit(ceiling(x), x, -2, "+") == -1
    assert limit(ceiling(x), x, -2, "-") == -2
    assert limit(ceiling(x), x, -1, "+") == 0
    assert limit(ceiling(x), x, -1, "-") == -1
    assert limit(ceiling(x), x, 0, "+") == 1
    assert limit(ceiling(x), x, 0, "-") == 0
    assert limit(ceiling(x), x, 1, "+") == 2
    assert limit(ceiling(x), x, 1, "-") == 1
    assert limit(ceiling(x), x, 2, "+") == 3
    assert limit(ceiling(x), x, 2, "-") == 2
    assert limit(ceiling(x), x, 248, "+") == 249
    assert limit(ceiling(x), x, 248, "-") == 248

    # https://github.com/sympy/sympy/issues/14478
    assert limit(x*ceiling(3/x)/2, x, 0, '+') == Rational(3, 2)
    assert limit(ceiling(x + 1/2) - ceiling(x), x, oo) == AccumBounds(-S.Half, S(3)/2)


def test_ceiling():
    assert ceiling(x).series(x) == 1
    assert ceiling(-x).series(x) == 0
    assert ceiling(sin(x)).series(x) == 1
    assert ceiling(sin(-x)).series(x) == 0
    assert ceiling(1 - cos(x)).series(x) == 1
    assert ceiling(1 - cos(-x)).series(x) == 1
    assert ceiling(x).series(x, 2) == 3
    assert ceiling(-x).series(x, 2) == -2


def test_ceiling():

    assert ceiling(nan) is nan

    assert ceiling(oo) is oo
    assert ceiling(-oo) is -oo
    assert ceiling(zoo) is zoo

    assert ceiling(0) == 0

    assert ceiling(1) == 1
    assert ceiling(-1) == -1

    assert ceiling(I*log(asin(5)/abs(asin(5)))) == 1
    assert ceiling(-I*log(asin(7)/abs(asin(7)))) == -1

    assert ceiling(E) == 3
    assert ceiling(-E) == -2

    assert ceiling(2*E) == 6
    assert ceiling(-2*E) == -5

    assert ceiling(pi) == 4
    assert ceiling(-pi) == -3

    assert ceiling(S.Half) == 1
    assert ceiling(Rational(-1, 2)) == 0

    assert ceiling(Rational(7, 3)) == 3
    assert ceiling(-Rational(7, 3)) == -2

    assert ceiling(Float(17.0)) == 17
    assert ceiling(-Float(17.0)) == -17

    assert ceiling(Float(7.69)) == 8
    assert ceiling(-Float(7.69)) == -7

    assert ceiling(1/(m+1)) == S.One
    assert ceiling((m+2)/(m+1)) == Integer(2)
    assert ceiling(-1/(m+1)) == S.Zero
    assert ceiling((m+2)/(-m-1)) == S.NegativeOne

    assert ceiling(I) == I
    assert ceiling(-I) == -I
    e = ceiling(i)
    assert e.func is ceiling and e.args[0] == i

    assert ceiling(oo*I) == oo*I
    assert ceiling(-oo*I) == -oo*I
    assert ceiling(exp(I*pi/4)*oo) == exp(I*pi/4)*oo

    assert ceiling(2*I) == 2*I
    assert ceiling(-2*I) == -2*I

    assert ceiling(I/2) == I
    assert ceiling(-I/2) == 0

    assert ceiling(E + 17) == 20
    assert ceiling(pi + 2) == 6

    assert ceiling(E + pi) == 6
    assert ceiling(I + pi) == I + 4

    assert ceiling(ceiling(pi)) == 4
    assert ceiling(ceiling(y)) == ceiling(y)
    assert ceiling(ceiling(x)) == ceiling(x)

    assert unchanged(ceiling, x)
    assert unchanged(ceiling, 2*x)
    assert unchanged(ceiling, k*x)

    assert ceiling(k) == k
    assert ceiling(2*k) == 2*k
    assert ceiling(k*n) == k*n

    assert unchanged(ceiling, k/2)

    assert unchanged(ceiling, x + y)

    assert ceiling(x + 3) == ceiling(x) + 3
    assert ceiling(x + 3.0) == ceiling(x) + 3
    assert ceiling(x + 3.0*I) == ceiling(x) + 3*I
    assert ceiling(x + k) == ceiling(x) + k

    assert ceiling(y + 3) == ceiling(y) + 3
    assert ceiling(y + k) == ceiling(y) + k

    assert ceiling(3 + pi + y*I) == 7 + ceiling(y)*I

    assert ceiling(k + n) == k + n

    assert unchanged(ceiling, x*I)
    assert ceiling(k*I) == k*I

    assert ceiling(Rational(23, 10) - E*I) == 3 - 2*I

    assert ceiling(sin(1)) == 1
    assert ceiling(sin(-1)) == 0

    assert ceiling(exp(2)) == 8

    assert ceiling(-log(8)/log(2)) != -2
    assert int(ceiling(-log(8)/log(2)).evalf(chop=True)) == -3

    assert ceiling(factorial(50)/exp(1)) == \
        11188719610782480504630258070757734324011354208865721592720336801

    assert (ceiling(y) >= y) == True
    assert (ceiling(y) > y).is_Relational
    assert (ceiling(y) < y) == False
    assert (ceiling(y) <= y).is_Relational
    assert (ceiling(x) >= x).is_Relational  # x could be non-real
    assert (ceiling(x) < x).is_Relational
    assert (ceiling(x) >= y).is_Relational  # arg is not same as rhs
    assert (ceiling(x) < y).is_Relational
    assert (ceiling(y) >= -oo) == True
    assert (ceiling(y) > -oo) == True
    assert (ceiling(y) <= oo) == True
    assert (ceiling(y) < oo) == True
    assert (ceiling(b) < b) == False
    assert (ceiling(b) <= b) == False
    assert (ceiling(b) > b) == True
    assert (ceiling(b) >= b) == True

    assert ceiling(y).rewrite(floor) == -floor(-y)
    assert ceiling(y).rewrite(frac) == y + frac(-y)
    assert ceiling(y).rewrite(floor).subs(y, -pi) == -floor(pi)
    assert ceiling(y).rewrite(floor).subs(y, E) == -floor(-E)
    assert ceiling(y).rewrite(frac).subs(y, pi) == ceiling(pi)
    assert ceiling(y).rewrite(frac).subs(y, -E) == ceiling(-E)

    assert Eq(ceiling(y), y + frac(-y))
    assert Eq(ceiling(y), -floor(-y))

    neg = Symbol('neg', negative=True)
    nn = Symbol('nn', nonnegative=True)
    pos = Symbol('pos', positive=True)
    np = Symbol('np', nonpositive=True)

    assert (ceiling(neg) <= 0) == True
    assert (ceiling(neg) < 0) == (neg <= -1)
    assert (ceiling(neg) > 0) == False
    assert (ceiling(neg) >= 0) == (neg > -1)
    assert (ceiling(neg) > -3) == (neg > -3)
    assert (ceiling(neg) <= 10) == (neg <= 10)

    assert (ceiling(nn) < 0) == False
    assert (ceiling(nn) >= 0) == True

    assert (ceiling(pos) < 0) == False
    assert (ceiling(pos) <= 0) == False
    assert (ceiling(pos) > 0) == True
    assert (ceiling(pos) >= 0) == True
    assert (ceiling(pos) >= 1) == True
    assert (ceiling(pos) > 5) == (pos > 5)

    assert (ceiling(np) <= 0) == True
    assert (ceiling(np) > 0) == False

    assert ceiling(neg).is_positive == False
    assert ceiling(neg).is_nonpositive == True
    assert ceiling(nn).is_positive is None
    assert ceiling(nn).is_nonpositive is None
    assert ceiling(pos).is_positive == True
    assert ceiling(pos).is_nonpositive == False
    assert ceiling(np).is_positive == False
    assert ceiling(np).is_nonpositive == True

    assert (ceiling(7, evaluate=False) >= 7) == True
    assert (ceiling(7, evaluate=False) > 7) == False
    assert (ceiling(7, evaluate=False) <= 7) == True
    assert (ceiling(7, evaluate=False) < 7) == False

    assert (ceiling(7, evaluate=False) >= 6) == True
    assert (ceiling(7, evaluate=False) > 6) == True
    assert (ceiling(7, evaluate=False) <= 6) == False
    assert (ceiling(7, evaluate=False) < 6) == False

    assert (ceiling(7, evaluate=False) >= 8) == False
    assert (ceiling(7, evaluate=False) > 8) == False
    assert (ceiling(7, evaluate=False) <= 8) == True
    assert (ceiling(7, evaluate=False) < 8) == True

    assert (ceiling(x) <= 5.5) == Le(ceiling(x), 5.5, evaluate=False)
    assert (ceiling(x) >= -3.2) == Ge(ceiling(x), -3.2, evaluate=False)
    assert (ceiling(x) < 2.9) == Lt(ceiling(x), 2.9, evaluate=False)
    assert (ceiling(x) > -1.7) == Gt(ceiling(x), -1.7, evaluate=False)

    assert (ceiling(y) <= 5.5) == (y <= 5)
    assert (ceiling(y) >= -3.2) == (y > -4)
    assert (ceiling(y) < 2.9) == (y <= 2)
    assert (ceiling(y) > -1.7) == (y > -2)

    assert (ceiling(y) <= n) == (y <= n)
    assert (ceiling(y) >= n) == (y > n - 1)
    assert (ceiling(y) < n) == (y <= n - 1)
    assert (ceiling(y) > n) == (y > n)

    assert ceiling(RootOf(x**3 - 27*x, 2)) == 6
    s = ImageSet(Lambda(n, n + (CRootOf(x**5 - x**2 + 1, 0))), Integers)
    f = CRootOf(x**5 - x**2 + 1, 0)
    s = ImageSet(Lambda(n, n + f), Integers)
    assert s.intersect(Interval(-10, 10)) == {i + f for i in range(-9, 11)}

