
def test_imaginary():
    i = sqrt(-1)
    assert latex(i) == r'i'


def test_imaginary():
    x = Symbol('x')
    lines = [
        '      1 |                                                     ..',
        '        |                                                   ..  ',
        '        |                                                ...    ',
        '        |                                              ..       ',
        '        |                                            ..         ',
        '        |                                          ..           ',
        '        |                                        ..             ',
        '        |                                      ..               ',
        '        |                                    ..                 ',
        '        |                                   /                   ',
        '    0.5 |----------------------------------/--------------------',
        '        |                                ..                     ',
        '        |                               /                       ',
        '        |                              .                        ',
        '        |                                                       ',
        '        |                             .                         ',
        '        |                            .                          ',
        '        |                                                       ',
        '        |                                                       ',
        '        |                                                       ',
        '      0 |_______________________________________________________',
        '         -1                         0                          1'
    ]
    # RuntimeWarning: invalid value encountered in sqrt
    with ignore_warnings(RuntimeWarning):
        assert list(textplot_str(sqrt(x), -1, 1)) == lines

    lines = [
        '      1 |                                                       ',
        '        |                                                       ',
        '        |                                                       ',
        '        |                                                       ',
        '        |                                                       ',
        '        |                                                       ',
        '        |                                                       ',
        '        |                                                       ',
        '        |                                                       ',
        '        |                                                       ',
        '      0 |-------------------------------------------------------',
        '        |                                                       ',
        '        |                                                       ',
        '        |                                                       ',
        '        |                                                       ',
        '        |                                                       ',
        '        |                                                       ',
        '        |                                                       ',
        '        |                                                       ',
        '        |                                                       ',
        '     -1 |_______________________________________________________',
        '         -1                         0                          1'
    ]
    assert list(textplot_str(S.ImaginaryUnit, -1, 1)) == lines


def test_imaginary():
    assert ask(Q.imaginary(x)) is None
    assert ask(Q.imaginary(x), Q.real(x)) is False
    assert ask(Q.imaginary(x), Q.prime(x)) is False

    assert ask(Q.imaginary(x + 1), Q.real(x)) is False
    assert ask(Q.imaginary(x + 1), Q.imaginary(x)) is False
    assert ask(Q.imaginary(x + I), Q.real(x)) is False
    assert ask(Q.imaginary(x + I), Q.imaginary(x)) is True
    assert ask(Q.imaginary(x + y), Q.imaginary(x) & Q.imaginary(y)) is True
    assert ask(Q.imaginary(x + y), Q.real(x) & Q.real(y)) is False
    assert ask(Q.imaginary(x + y), Q.imaginary(x) & Q.real(y)) is False
    assert ask(Q.imaginary(x + y), Q.complex(x) & Q.real(y)) is None
    assert ask(
        Q.imaginary(x + y + z), Q.real(x) & Q.real(y) & Q.real(z)) is False
    assert ask(Q.imaginary(x + y + z),
        Q.real(x) & Q.real(y) & Q.imaginary(z)) is None
    assert ask(Q.imaginary(x + y + z),
        Q.real(x) & Q.imaginary(y) & Q.imaginary(z)) is False

    assert ask(Q.imaginary(I*x), Q.real(x)) is True
    assert ask(Q.imaginary(I*x), Q.imaginary(x)) is False
    assert ask(Q.imaginary(I*x), Q.complex(x)) is None
    assert ask(Q.imaginary(x*y), Q.imaginary(x) & Q.real(y)) is True
    assert ask(Q.imaginary(x*y), Q.real(x) & Q.real(y)) is False

    assert ask(Q.imaginary(I**x), Q.negative(x)) is None
    assert ask(Q.imaginary(I**x), Q.positive(x)) is None
    assert ask(Q.imaginary(I**x), Q.even(x)) is False
    assert ask(Q.imaginary(I**x), Q.odd(x)) is True
    assert ask(Q.imaginary(I**x), Q.imaginary(x)) is False
    assert ask(Q.imaginary((2*I)**x), Q.imaginary(x)) is False
    assert ask(Q.imaginary(x**0), Q.imaginary(x)) is False
    assert ask(Q.imaginary(x**y), Q.imaginary(x) & Q.imaginary(y)) is None
    assert ask(Q.imaginary(x**y), Q.imaginary(x) & Q.real(y)) is None
    assert ask(Q.imaginary(x**y), Q.real(x) & Q.imaginary(y)) is None
    assert ask(Q.imaginary(x**y), Q.real(x) & Q.real(y)) is None
    assert ask(Q.imaginary(x**y), Q.imaginary(x) & Q.integer(y)) is None
    assert ask(Q.imaginary(x**y), Q.imaginary(y) & Q.integer(x)) is None
    assert ask(Q.imaginary(x**y), Q.imaginary(x) & Q.odd(y)) is True
    assert ask(Q.imaginary(x**y), Q.imaginary(x) & Q.rational(y)) is None
    assert ask(Q.imaginary(x**y), Q.imaginary(x) & Q.even(y)) is False

    assert ask(Q.imaginary(x**y), Q.real(x) & Q.integer(y)) is False
    assert ask(Q.imaginary(x**y), Q.positive(x) & Q.real(y)) is False
    assert ask(Q.imaginary(x**y), Q.negative(x) & Q.real(y)) is None
    assert ask(Q.imaginary(x**y), Q.negative(x) & Q.real(y) & ~Q.rational(y)) is False
    assert ask(Q.imaginary(x**y), Q.integer(x) & Q.imaginary(y)) is None
    assert ask(Q.imaginary(x**y), Q.negative(x) & Q.rational(y) & Q.integer(2*y)) is True
    assert ask(Q.imaginary(x**y), Q.negative(x) & Q.rational(y) & ~Q.integer(2*y)) is False
    assert ask(Q.imaginary(x**y), Q.negative(x) & Q.rational(y)) is None
    assert ask(Q.imaginary(x**y), Q.real(x) & Q.rational(y) & ~Q.integer(2*y)) is False
    assert ask(Q.imaginary(x**y), Q.real(x) & Q.rational(y) & Q.integer(2*y)) is None

    # logarithm
    assert ask(Q.imaginary(log(I))) is True
    assert ask(Q.imaginary(log(2*I))) is False
    assert ask(Q.imaginary(log(I + 1))) is False
    assert ask(Q.imaginary(log(x)), Q.complex(x)) is None
    assert ask(Q.imaginary(log(x)), Q.imaginary(x)) is None
    assert ask(Q.imaginary(log(x)), Q.positive(x)) is False
    assert ask(Q.imaginary(log(exp(x))), Q.complex(x)) is None
    assert ask(Q.imaginary(log(exp(x))), Q.imaginary(x)) is None  # zoo/I/a+I*b
    assert ask(Q.imaginary(log(exp(I)))) is True

    # exponential
    assert ask(Q.imaginary(exp(x)**x), Q.imaginary(x)) is False
    eq = Pow(exp(pi*I*x, evaluate=False), x, evaluate=False)
    assert ask(Q.imaginary(eq), Q.even(x)) is False
    eq = Pow(exp(pi*I*x/2, evaluate=False), x, evaluate=False)
    assert ask(Q.imaginary(eq), Q.odd(x)) is True
    assert ask(Q.imaginary(exp(3*I*pi*x)**x), Q.integer(x)) is False
    assert ask(Q.imaginary(exp(2*pi*I, evaluate=False))) is False
    assert ask(Q.imaginary(exp(pi*I/2, evaluate=False))) is True

    # issue 7886
    assert ask(Q.imaginary(Pow(x, Rational(1, 4))), Q.real(x) & Q.negative(x)) is False


def test_imaginary():
    assert satask(Q.imaginary(2*I)) is True
    assert satask(Q.imaginary(x*y), Q.imaginary(x)) is None
    assert satask(Q.imaginary(x*y), Q.imaginary(x) & Q.real(y)) is True
    assert satask(Q.imaginary(x), Q.real(x)) is False
    assert satask(Q.imaginary(1)) is False
    assert satask(Q.imaginary(x*y), Q.real(x) & Q.real(y)) is False
    assert satask(Q.imaginary(x + y), Q.real(x) & Q.real(y)) is False

