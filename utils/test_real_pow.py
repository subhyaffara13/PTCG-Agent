
def test_real_pow():
    assert ask(Q.real(x**2), Q.real(x)) is True
    assert ask(Q.real(sqrt(x)), Q.negative(x)) is False
    assert ask(Q.real(x**y), Q.real(x) & Q.integer(y)) is None
    assert ask(Q.real(x**y), Q.real(x) & Q.real(y)) is None
    assert ask(Q.real(x**y), Q.positive(x) & Q.real(y)) is True
    assert ask(Q.real(x**y), Q.imaginary(x) & Q.imaginary(y)) is None  # I**I or (2*I)**I
    assert ask(Q.real(x**y), Q.imaginary(x) & Q.real(y)) is None  # I**1 or I**0
    assert ask(Q.real(x**y), Q.real(x) & Q.imaginary(y)) is None  # could be exp(2*pi*I) or 2**I
    assert ask(Q.real(x**0), Q.imaginary(x)) is True
    assert ask(Q.real(x**y), Q.positive(x) & Q.real(y)) is True
    assert ask(Q.real(x**y), Q.real(x) & Q.rational(y)) is None
    assert ask(Q.real(x**y), Q.imaginary(x) & Q.integer(y)) is None
    assert ask(Q.real(x**y), Q.imaginary(x) & Q.odd(y)) is False
    assert ask(Q.real(x**y), Q.imaginary(x) & Q.even(y)) is True
    assert ask(Q.real(x**(y/z)), Q.real(x) & Q.real(y/z) & Q.rational(y/z) & Q.even(z) & Q.positive(x)) is True
    assert ask(Q.real(x**(y/z)), Q.real(x) & Q.rational(y/z) & Q.even(z) & Q.negative(x)) is None
    assert ask(Q.real(x**(y/z)), Q.real(x) & Q.integer(y/z)) is None
    assert ask(Q.real(x**(y/z)), Q.real(x) & Q.real(y/z) & Q.positive(x)) is True
    assert ask(Q.real(x**(y/z)), Q.real(x) & Q.real(y/z) & Q.negative(x)) is None
    assert ask(Q.real((-I)**i), Q.imaginary(i)) is True
    assert ask(Q.real(I**i), Q.imaginary(i)) is True
    assert ask(Q.real(i**i), Q.imaginary(i)) is None  # i might be 2*I
    assert ask(Q.real(x**i), Q.imaginary(i)) is None  # x could be 0
    assert ask(Q.real(x**(I*pi/log(x))), Q.real(x)) is True

    # https://github.com/sympy/sympy/issues/27485
    assert ask(Q.real(n**p), Q.negative(n) & Q.positive(p)) is None

    # https://github.com/sympy/sympy/issues/16530
    assert ask(Q.real(1/Abs(x))) is None
    assert ask(Q.real(x**y), Q.zero(x) & Q.real(y)) is None
    assert ask(Q.real(x**y), Q.zero(x) & Q.positive(y)) is True

