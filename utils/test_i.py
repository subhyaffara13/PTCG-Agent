
def test_I():
    z = S.ImaginaryUnit
    assert z.is_commutative is True
    assert z.is_integer is False
    assert z.is_rational is False
    assert z.is_algebraic is True
    assert z.is_transcendental is False
    assert z.is_real is False
    assert z.is_complex is True
    assert z.is_noninteger is False
    assert z.is_irrational is False
    assert z.is_imaginary is True
    assert z.is_positive is False
    assert z.is_negative is False
    assert z.is_nonpositive is False
    assert z.is_nonnegative is False
    assert z.is_even is False
    assert z.is_odd is False
    assert z.is_finite is True
    assert z.is_infinite is False
    assert z.is_comparable is False
    assert z.is_prime is False
    assert z.is_composite is False


def test_I():
    z = I
    assert ask(Q.commutative(z)) is True
    assert ask(Q.integer(z)) is False
    assert ask(Q.rational(z)) is False
    assert ask(Q.algebraic(z)) is True
    assert ask(Q.real(z)) is False
    assert ask(Q.complex(z)) is True
    assert ask(Q.irrational(z)) is False
    assert ask(Q.imaginary(z)) is True
    assert ask(Q.positive(z)) is False
    assert ask(Q.negative(z)) is False
    assert ask(Q.even(z)) is False
    assert ask(Q.odd(z)) is False
    assert ask(Q.finite(z)) is True
    assert ask(Q.prime(z)) is False
    assert ask(Q.composite(z)) is False
    assert ask(Q.hermitian(z)) is False
    assert ask(Q.antihermitian(z)) is True

    z = 1 + I
    assert ask(Q.commutative(z)) is True
    assert ask(Q.integer(z)) is False
    assert ask(Q.rational(z)) is False
    assert ask(Q.algebraic(z)) is True
    assert ask(Q.real(z)) is False
    assert ask(Q.complex(z)) is True
    assert ask(Q.irrational(z)) is False
    assert ask(Q.imaginary(z)) is False
    assert ask(Q.positive(z)) is False
    assert ask(Q.negative(z)) is False
    assert ask(Q.even(z)) is False
    assert ask(Q.odd(z)) is False
    assert ask(Q.finite(z)) is True
    assert ask(Q.prime(z)) is False
    assert ask(Q.composite(z)) is False
    assert ask(Q.hermitian(z)) is False
    assert ask(Q.antihermitian(z)) is False

    z = I*(1 + I)
    assert ask(Q.commutative(z)) is True
    assert ask(Q.integer(z)) is False
    assert ask(Q.rational(z)) is False
    assert ask(Q.algebraic(z)) is True
    assert ask(Q.real(z)) is False
    assert ask(Q.complex(z)) is True
    assert ask(Q.irrational(z)) is False
    assert ask(Q.imaginary(z)) is False
    assert ask(Q.positive(z)) is False
    assert ask(Q.negative(z)) is False
    assert ask(Q.even(z)) is False
    assert ask(Q.odd(z)) is False
    assert ask(Q.finite(z)) is True
    assert ask(Q.prime(z)) is False
    assert ask(Q.composite(z)) is False
    assert ask(Q.hermitian(z)) is False
    assert ask(Q.antihermitian(z)) is False

    z = I**(I)
    assert ask(Q.imaginary(z)) is False
    assert ask(Q.real(z)) is True

    z = (-I)**(I)
    assert ask(Q.imaginary(z)) is False
    assert ask(Q.real(z)) is True

    z = (3*I)**(I)
    assert ask(Q.imaginary(z)) is False
    assert ask(Q.real(z)) is False

    z = (1)**(I)
    assert ask(Q.imaginary(z)) is False
    assert ask(Q.real(z)) is True

    z = (-1)**(I)
    assert ask(Q.imaginary(z)) is False
    assert ask(Q.real(z)) is True

    z = (1+I)**(I)
    assert ask(Q.imaginary(z)) is False
    assert ask(Q.real(z)) is False

    z = (I)**(I+3)
    assert ask(Q.imaginary(z)) is True
    assert ask(Q.real(z)) is False

    z = (I)**(I+2)
    assert ask(Q.imaginary(z)) is False
    assert ask(Q.real(z)) is True

    z = (I)**(2)
    assert ask(Q.imaginary(z)) is False
    assert ask(Q.real(z)) is True

    z = (I)**(3)
    assert ask(Q.imaginary(z)) is True
    assert ask(Q.real(z)) is False

    z = (3)**(I)
    assert ask(Q.imaginary(z)) is False
    assert ask(Q.real(z)) is False

    z = (I)**(0)
    assert ask(Q.imaginary(z)) is False
    assert ask(Q.real(z)) is True

