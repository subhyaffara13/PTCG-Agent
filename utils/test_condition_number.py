
def test_condition_number():
    x = Symbol('x', real=True)
    A = eye(3)
    A[0, 0] = 10
    A[2, 2] = Rational(1, 10)
    assert A.condition_number() == 100

    A[1, 1] = x
    assert A.condition_number() == Max(10, Abs(x)) / Min(Rational(1, 10), Abs(x))

    M = Matrix([[cos(x), sin(x)], [-sin(x), cos(x)]])
    Mc = M.condition_number()
    assert all(Float(1.).epsilon_eq(Mc.subs(x, val).evalf()) for val in
        [Rational(1, 5), S.Half, Rational(1, 10), pi/2, pi, pi*Rational(7, 4) ])

    #issue 10782
    assert Matrix([]).condition_number() == 0


def test_condition_number():
    x = Symbol('x', real=True)
    A = eye(3)
    A[0, 0] = 10
    A[2, 2] = Rational(1, 10)
    assert A.condition_number() == 100

    A[1, 1] = x
    assert A.condition_number() == Max(10, Abs(x)) / Min(Rational(1, 10), Abs(x))

    M = Matrix([[cos(x), sin(x)], [-sin(x), cos(x)]])
    Mc = M.condition_number()
    assert all(Float(1.).epsilon_eq(Mc.subs(x, val).evalf()) for val in
        [Rational(1, 5), S.Half, Rational(1, 10), pi/2, pi, pi*Rational(7, 4) ])

    #issue 10782
    assert Matrix([]).condition_number() == 0

