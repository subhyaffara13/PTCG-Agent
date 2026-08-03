import re

def test_arg():
    assert arg(0) is nan
    assert arg(1) == 0
    assert arg(-1) == pi
    assert arg(I) == pi/2
    assert arg(-I) == -pi/2
    assert arg(1 + I) == pi/4
    assert arg(-1 + I) == pi*Rational(3, 4)
    assert arg(1 - I) == -pi/4
    assert arg(exp_polar(4*pi*I)) == 4*pi
    assert arg(exp_polar(-7*pi*I)) == -7*pi
    assert arg(exp_polar(5 - 3*pi*I/4)) == pi*Rational(-3, 4)

    assert arg(exp(I*pi/7)) == pi/7     # issue 17300
    assert arg(exp(16*I)) == 16 - 6*pi
    assert arg(exp(13*I*pi/12)) == -11*pi/12
    assert arg(exp(123 - 5*I)) == -5 + 2*pi
    assert arg(exp(sin(1 + 3*I))) == -2*pi + cos(1)*sinh(3)
    r = Symbol('r', real=True)
    assert arg(exp(r - 2*I)) == -2

    f = Function('f')
    assert not arg(f(0) + I*f(1)).atoms(re)

    # check nesting
    x = Symbol('x')
    assert arg(arg(arg(x))) is not S.NaN
    assert arg(arg(arg(arg(x)))) is S.NaN
    r = Symbol('r', extended_real=True)
    assert arg(arg(r)) is not S.NaN
    assert arg(arg(arg(r))) is S.NaN

    p = Function('p', extended_positive=True)
    assert arg(p(x)) == 0
    assert arg((3 + I)*p(x)) == arg(3  + I)

    p = Symbol('p', positive=True)
    assert arg(p) == 0
    assert arg(p*I) == pi/2

    n = Symbol('n', negative=True)
    assert arg(n) == pi
    assert arg(n*I) == -pi/2

    x = Symbol('x')
    assert conjugate(arg(x)) == arg(x)

    e = p + I*p**2
    assert arg(e) == arg(1 + p*I)
    # make sure sign doesn't swap
    e = -2*p + 4*I*p**2
    assert arg(e) == arg(-1 + 2*p*I)
    # make sure sign isn't lost
    x = symbols('x', real=True)  # could be zero
    e = x + I*x
    assert arg(e) == arg(x*(1 + I))
    assert arg(e/p) == arg(x*(1 + I))
    e = p*cos(p) + I*log(p)*exp(p)
    assert arg(e).args[0] == e
    # keep it simple -- let the user do more advanced cancellation
    e = (p + 1) + I*(p**2 - 1)
    assert arg(e).args[0] == e

    f = Function('f')
    e = 2*x*(f(0) - 1) - 2*x*f(0)
    assert arg(e) == arg(-2*x)
    assert arg(f(0)).func == arg and arg(f(0)).args == (f(0),)


def test_arg():
    x = Symbol('x', complex = True)
    assert refine(arg(x), Q.positive(x)) == 0
    assert refine(arg(x), Q.negative(x)) == pi

