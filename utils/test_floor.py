
def test_floor():
    assert limit(floor(x), x, -2, "+") == -2
    assert limit(floor(x), x, -2, "-") == -3
    assert limit(floor(x), x, -1, "+") == -1
    assert limit(floor(x), x, -1, "-") == -2
    assert limit(floor(x), x, 0, "+") == 0
    assert limit(floor(x), x, 0, "-") == -1
    assert limit(floor(x), x, 1, "+") == 1
    assert limit(floor(x), x, 1, "-") == 0
    assert limit(floor(x), x, 2, "+") == 2
    assert limit(floor(x), x, 2, "-") == 1
    assert limit(floor(x), x, 248, "+") == 248
    assert limit(floor(x), x, 248, "-") == 247

    # https://github.com/sympy/sympy/issues/14478
    assert limit(x*floor(3/x)/2, x, 0, '+') == Rational(3, 2)
    assert limit(floor(x + 1/2) - floor(x), x, oo) == AccumBounds(-S.Half, S(3)/2)

    # test issue 9158
    assert limit(floor(atan(x)), x, oo) == 1
    assert limit(floor(atan(x)), x, -oo) == -2
    assert limit(ceiling(atan(x)), x, oo) == 2
    assert limit(ceiling(atan(x)), x, -oo) == -1


def test_floor():
    x = Symbol('x')
    assert floor(x).series(x) == 0
    assert floor(-x).series(x) == -1
    assert floor(sin(x)).series(x) == 0
    assert floor(sin(-x)).series(x) == -1
    assert floor(x**3).series(x) == 0
    assert floor(-x**3).series(x) == -1
    assert floor(cos(x)).series(x) == 0
    assert floor(cos(-x)).series(x) == 0
    assert floor(5 + sin(x)).series(x) == 5
    assert floor(5 + sin(-x)).series(x) == 4

    assert floor(x).series(x, 2) == 2
    assert floor(-x).series(x, 2) == -3

    x = Symbol('x', negative=True)
    assert floor(x + 1.5).series(x) == 1


def test_floor():
    a = floor(interval(0.2, 0.5))
    assert a.start == 0
    assert a.end == 0

    a = floor(interval(0.5, 1.5))
    assert a.start == 0
    assert a.end == 1
    assert a.is_valid is None

    a = floor(interval(-5, 5))
    assert a.is_valid is None

    a = floor(5.4)
    assert a.start == 5
    assert a.end == 5


def test_floor():

    assert floor(nan) is nan

    assert floor(oo) is oo
    assert floor(-oo) is -oo
    assert floor(zoo) is zoo

    assert floor(0) == 0

    assert floor(1) == 1
    assert floor(-1) == -1

    assert floor(I*log(asin(5)/abs(asin(5)))) == 0
    assert floor(-I*log(asin(7)/abs(asin(7)))) == -2

    assert floor(E) == 2
    assert floor(-E) == -3

    assert floor(2*E) == 5
    assert floor(-2*E) == -6

    assert floor(pi) == 3
    assert floor(-pi) == -4

    assert floor(S.Half) == 0
    assert floor(Rational(-1, 2)) == -1

    assert floor(Rational(7, 3)) == 2
    assert floor(Rational(-7, 3)) == -3
    assert floor(-Rational(7, 3)) == -3

    assert floor(Float(17.0)) == 17
    assert floor(-Float(17.0)) == -17

    assert floor(Float(7.69)) == 7
    assert floor(-Float(7.69)) == -8

    assert floor(1/(m+1)) == S.Zero
    assert floor((m+2)/(m+1)) == S.One
    assert floor(-1/(m+1)) == S.NegativeOne
    assert floor((m+2)/(-m-1)) == Integer(-2)

    assert floor(I) == I
    assert floor(-I) == -I
    e = floor(i)
    assert e.func is floor and e.args[0] == i

    assert floor(oo*I) == oo*I
    assert floor(-oo*I) == -oo*I
    assert floor(exp(I*pi/4)*oo) == exp(I*pi/4)*oo

    assert floor(2*I) == 2*I
    assert floor(-2*I) == -2*I

    assert floor(I/2) == 0
    assert floor(-I/2) == -I

    assert floor(E + 17) == 19
    assert floor(pi + 2) == 5

    assert floor(E + pi) == 5
    assert floor(I + pi) == 3 + I

    assert floor(floor(pi)) == 3
    assert floor(floor(y)) == floor(y)
    assert floor(floor(x)) == floor(x)

    assert unchanged(floor, x)
    assert unchanged(floor, 2*x)
    assert unchanged(floor, k*x)

    assert floor(k) == k
    assert floor(2*k) == 2*k
    assert floor(k*n) == k*n

    assert unchanged(floor, k/2)

    assert unchanged(floor, x + y)

    assert floor(x + 3) == floor(x) + 3
    assert floor(x + k) == floor(x) + k

    assert floor(y + 3) == floor(y) + 3
    assert floor(y + k) == floor(y) + k

    assert floor(3 + I*y + pi) == 6 + floor(y)*I

    assert floor(k + n) == k + n

    assert unchanged(floor, x*I)
    assert floor(k*I) == k*I

    assert floor(Rational(23, 10) - E*I) == 2 - 3*I

    assert floor(sin(1)) == 0
    assert floor(sin(-1)) == -1

    assert floor(exp(2)) == 7

    assert floor(log(8)/log(2)) != 2
    assert int(floor(log(8)/log(2)).evalf(chop=True)) == 3

    assert floor(factorial(50)/exp(1)) == \
        11188719610782480504630258070757734324011354208865721592720336800

    assert (floor(y) < y).is_Relational
    assert (floor(y) <= y) == True
    assert (floor(y) > y) == False
    assert (floor(y) >= y).is_Relational
    assert (floor(x) <= x).is_Relational  # x could be non-real
    assert (floor(x) > x).is_Relational
    assert (floor(x) <= y).is_Relational  # arg is not same as rhs
    assert (floor(x) > y).is_Relational
    assert (floor(y) <= oo) == True
    assert (floor(y) < oo) == True
    assert (floor(y) >= -oo) == True
    assert (floor(y) > -oo) == True
    assert (floor(b) < b) == True
    assert (floor(b) <= b) == True
    assert (floor(b) > b) == False
    assert (floor(b) >= b) == False

    assert floor(y).rewrite(frac) == y - frac(y)
    assert floor(y).rewrite(ceiling) == -ceiling(-y)
    assert floor(y).rewrite(frac).subs(y, -pi) == floor(-pi)
    assert floor(y).rewrite(frac).subs(y, E) == floor(E)
    assert floor(y).rewrite(ceiling).subs(y, E) == -ceiling(-E)
    assert floor(y).rewrite(ceiling).subs(y, -pi) == -ceiling(pi)

    assert Eq(floor(y), y - frac(y))
    assert Eq(floor(y), -ceiling(-y))

    neg = Symbol('neg', negative=True)
    nn = Symbol('nn', nonnegative=True)
    pos = Symbol('pos', positive=True)
    np = Symbol('np', nonpositive=True)

    assert (floor(neg) < 0) == True
    assert (floor(neg) <= 0) == True
    assert (floor(neg) > 0) == False
    assert (floor(neg) >= 0) == False
    assert (floor(neg) <= -1) == True
    assert (floor(neg) >= -3) == (neg >= -3)
    assert (floor(neg) < 5) == (neg < 5)

    assert (floor(nn) < 0) == False
    assert (floor(nn) >= 0) == True

    assert (floor(pos) < 0) == False
    assert (floor(pos) <= 0) == (pos < 1)
    assert (floor(pos) > 0) == (pos >= 1)
    assert (floor(pos) >= 0) == True
    assert (floor(pos) >= 3) == (pos >= 3)

    assert (floor(np) <= 0) == True
    assert (floor(np) > 0) == False

    assert floor(neg).is_negative == True
    assert floor(neg).is_nonnegative == False
    assert floor(nn).is_negative == False
    assert floor(nn).is_nonnegative == True
    assert floor(pos).is_negative == False
    assert floor(pos).is_nonnegative == True
    assert floor(np).is_negative is None
    assert floor(np).is_nonnegative is None

    assert (floor(7, evaluate=False) >= 7) == True
    assert (floor(7, evaluate=False) > 7) == False
    assert (floor(7, evaluate=False) <= 7) == True
    assert (floor(7, evaluate=False) < 7) == False

    assert (floor(7, evaluate=False) >= 6) == True
    assert (floor(7, evaluate=False) > 6) == True
    assert (floor(7, evaluate=False) <= 6) == False
    assert (floor(7, evaluate=False) < 6) == False

    assert (floor(7, evaluate=False) >= 8) == False
    assert (floor(7, evaluate=False) > 8) == False
    assert (floor(7, evaluate=False) <= 8) == True
    assert (floor(7, evaluate=False) < 8) == True

    assert (floor(x) <= 5.5) == Le(floor(x), 5.5, evaluate=False)
    assert (floor(x) >= -3.2) == Ge(floor(x), -3.2, evaluate=False)
    assert (floor(x) < 2.9) == Lt(floor(x), 2.9, evaluate=False)
    assert (floor(x) > -1.7) == Gt(floor(x), -1.7, evaluate=False)

    assert (floor(y) <= 5.5) == (y < 6)
    assert (floor(y) >= -3.2) == (y >= -3)
    assert (floor(y) < 2.9) == (y < 3)
    assert (floor(y) > -1.7) == (y >= -1)

    assert (floor(y) <= n) == (y < n + 1)
    assert (floor(y) >= n) == (y >= n)
    assert (floor(y) < n) == (y < n)
    assert (floor(y) > n) == (y >= n + 1)

    assert floor(RootOf(x**3 - 27*x, 2)) == 5

