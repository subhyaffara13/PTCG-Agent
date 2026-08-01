
def test_real_functions():
    # trigonometric functions
    assert ask(Q.real(sin(x))) is None
    assert ask(Q.real(cos(x))) is None
    assert ask(Q.real(sin(x)), Q.real(x)) is True
    assert ask(Q.real(cos(x)), Q.real(x)) is True

    # exponential function
    assert ask(Q.real(exp(x))) is None
    assert ask(Q.real(exp(x)), Q.real(x)) is True
    assert ask(Q.real(x + exp(x)), Q.real(x)) is True
    assert ask(Q.real(exp(2*pi*I, evaluate=False))) is True
    assert ask(Q.real(exp(pi*I, evaluate=False))) is True
    assert ask(Q.real(exp(pi*I/2, evaluate=False))) is False

    # logarithm
    assert ask(Q.real(log(I))) is False
    assert ask(Q.real(log(2*I))) is False
    assert ask(Q.real(log(I + 1))) is False
    assert ask(Q.real(log(x)), Q.complex(x)) is None
    assert ask(Q.real(log(x)), Q.imaginary(x)) is False
    assert ask(Q.real(log(exp(x))), Q.imaginary(x)) is None  # exp(2*pi*I) is 1, log(exp(pi*I)) is pi*I (disregarding periodicity)
    assert ask(Q.real(log(exp(x))), Q.complex(x)) is None
    eq = Pow(exp(2*pi*I*x, evaluate=False), x, evaluate=False)
    assert ask(Q.real(eq), Q.integer(x)) is True
    assert ask(Q.real(exp(x)**x), Q.imaginary(x)) is True
    assert ask(Q.real(exp(x)**x), Q.complex(x)) is None

    # Q.complexes
    assert ask(Q.real(re(x))) is True
    assert ask(Q.real(im(x))) is True

