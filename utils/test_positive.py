
def test_positive():
    assert ask(Q.positive(cos(I) ** 2 + sin(I) ** 2 - 1)) is None
    assert ask(Q.positive(x), Q.positive(x)) is True
    assert ask(Q.positive(x), Q.negative(x)) is False
    assert ask(Q.positive(x), Q.nonzero(x)) is None

    assert ask(Q.positive(-x), Q.positive(x)) is False
    assert ask(Q.positive(-x), Q.negative(x)) is True

    assert ask(Q.positive(x + y), Q.positive(x) & Q.positive(y)) is True
    assert ask(Q.positive(x + y), Q.positive(x) & Q.nonnegative(y)) is True
    assert ask(Q.positive(x + y), Q.positive(x) & Q.negative(y)) is None
    assert ask(Q.positive(x + y), Q.positive(x) & Q.imaginary(y)) is False

    assert ask(Q.positive(2*x), Q.positive(x)) is True
    assumptions = Q.positive(x) & Q.negative(y) & Q.negative(z) & Q.positive(w)
    assert ask(Q.positive(x*y*z)) is None
    assert ask(Q.positive(x*y*z), assumptions) is True
    assert ask(Q.positive(-x*y*z), assumptions) is False

    assert ask(Q.positive(x**I), Q.positive(x)) is None

    assert ask(Q.positive(x**2), Q.positive(x)) is True
    assert ask(Q.positive(x**2), Q.negative(x)) is True
    assert ask(Q.positive(x**3), Q.negative(x)) is False
    assert ask(Q.positive(1/(1 + x**2)), Q.real(x)) is True
    assert ask(Q.positive(2**I)) is False
    assert ask(Q.positive(2 + I)) is False
    # although this could be False, it is representative of expressions
    # that don't evaluate to a zero with precision
    assert ask(Q.positive(cos(I)**2 + sin(I)**2 - 1)) is None
    assert ask(Q.positive(-I + I*(cos(2)**2 + sin(2)**2))) is None

    #exponential
    assert ask(Q.positive(exp(x)), Q.real(x)) is True
    assert ask(~Q.negative(exp(x)), Q.real(x)) is True
    assert ask(Q.positive(x + exp(x)), Q.real(x)) is None
    assert ask(Q.positive(exp(x)), Q.imaginary(x)) is None
    assert ask(Q.positive(exp(2*pi*I, evaluate=False)), Q.imaginary(x)) is True
    assert ask(Q.negative(exp(pi*I, evaluate=False)), Q.imaginary(x)) is True
    assert ask(Q.positive(exp(x*pi*I)), Q.even(x)) is True
    assert ask(Q.positive(exp(x*pi*I)), Q.odd(x)) is False
    assert ask(Q.positive(exp(x*pi*I)), Q.real(x)) is None

    # logarithm
    assert ask(Q.positive(log(x)), Q.imaginary(x)) is False
    assert ask(Q.positive(log(x)), Q.negative(x)) is False
    assert ask(Q.positive(log(x)), Q.positive(x)) is None
    assert ask(Q.positive(log(x + 2)), Q.positive(x)) is True

    # factorial
    assert ask(Q.positive(factorial(x)), Q.integer(x) & Q.positive(x))
    assert ask(Q.positive(factorial(x)), Q.integer(x)) is None

    #absolute value
    assert ask(Q.positive(Abs(x))) is None  # Abs(0) = 0
    assert ask(Q.positive(Abs(x)), Q.positive(x)) is True

