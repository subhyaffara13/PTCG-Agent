import re

def test_issues_6819_6820_6821_6248_8692_25777_25779():
    # issue 6821
    x, y = symbols('x y', real=True)
    assert solve(abs(x + 3) - 2*abs(x - 3)) == [1, 9]
    assert solve([abs(x) - 2, arg(x) - pi], x) == [(-2,)]
    assert set(solve(abs(x - 7) - 8)) == {-S.One, S(15)}

    # issue 8692
    assert solve(Eq(Abs(x + 1) + Abs(x**2 - 7), 9), x) == [
        Rational(-1, 2) + sqrt(61)/2, -sqrt(69)/2 + S.Half]

    # issue 7145
    assert solve(2*abs(x) - abs(x - 1)) == [-1, Rational(1, 3)]

    # 25777
    assert solve(abs(x**3 + x + 2)/(x + 1)) == []

    # 25779
    assert solve(abs(x)) == [0]
    assert solve(Eq(abs(x**2 - 2*x), 4), x) == [
        1 - sqrt(5), 1 + sqrt(5)]
    nn = symbols('nn', nonnegative=True)
    assert solve(abs(sqrt(nn))) == [0]
    nz = symbols('nz', nonzero=True)
    assert solve(Eq(Abs(4 + 1 / (4*nz)), 0)) == [-Rational(1, 16)]

    x = symbols('x')
    assert solve([re(x) - 1, im(x) - 2], x) == [
        {x: 1 + 2*I, re(x): 1, im(x): 2}]

    # check for 'dict' handling of solution
    eq = sqrt(re(x)**2 + im(x)**2) - 3
    assert solve(eq) == solve(eq, x)

    i = symbols('i', imaginary=True)
    assert solve(abs(i) - 3) == [-3*I, 3*I]
    raises(NotImplementedError, lambda: solve(abs(x) - 3))

    w = symbols('w', integer=True)
    assert solve(2*x**w - 4*y**w, w) == solve((x/y)**w - 2, w)

    x, y = symbols('x y', real=True)
    assert solve(x + y*I + 3) == {y: 0, x: -3}
    # issue 2642
    assert solve(x*(1 + I)) == [0]

    x, y = symbols('x y', imaginary=True)
    assert solve(x + y*I + 3 + 2*I) == {x: -2*I, y: 3*I}

    x = symbols('x', real=True)
    assert solve(x + y + 3 + 2*I) == {x: -3, y: -2*I}

    # issue 6248
    f = Function('f')
    assert solve(f(x + 1) - f(2*x - 1)) == [2]
    assert solve(log(x + 1) - log(2*x - 1)) == [2]

    x = symbols('x')
    assert solve(2**x + 4**x) == [I*pi/log(2)]

