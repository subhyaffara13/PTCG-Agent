
def test_E():
    assert E(5) == 5


def test_E():
    assert E(z, 0) == z
    assert E(0, m) == 0
    assert E(i*pi/2, m) == i*E(m)
    assert E(z, oo) is zoo
    assert E(z, -oo) is zoo
    assert E(0) == pi/2
    assert E(1) == 1
    assert E(oo) == I*oo
    assert E(-oo) is oo
    assert E(zoo) is zoo

    assert E(-z, m) == -E(z, m)

    assert E(z, m).diff(z) == sqrt(1 - m*sin(z)**2)
    assert E(z, m).diff(m) == (E(z, m) - F(z, m))/(2*m)
    assert E(z).diff(z) == (E(z) - K(z))/(2*z)
    r = randcplx()
    assert td(E(r, m), m)
    assert td(E(z, r), z)
    assert td(E(z), z)

    mi = Symbol('m', real=False)
    assert E(z, mi).conjugate() == E(z.conjugate(), mi.conjugate())
    assert E(mi).conjugate() == E(mi.conjugate())
    mr = Symbol('m', negative=True)
    assert E(z, mr).conjugate() == E(z.conjugate(), mr)
    assert E(mr).conjugate() == E(mr)

    assert E(z).rewrite(hyper) == (pi/2)*hyper((Rational(-1, 2), S.Half), (S.One,), z)
    assert tn(E(z), (pi/2)*hyper((Rational(-1, 2), S.Half), (S.One,), z))
    assert E(z).rewrite(meijerg) == \
        -meijerg(((S.Half, Rational(3, 2)), []), ((S.Zero,), (S.Zero,)), -z)/4
    assert tn(E(z), -meijerg(((S.Half, Rational(3, 2)), []), ((S.Zero,), (S.Zero,)), -z)/4)

    assert E(z, m).series(z) == \
        z + z**5*(-m**2/40 + m/30) - m*z**3/6 + O(z**6)
    assert E(z).series(z) == pi/2 - pi*z/8 - 3*pi*z**2/128 - \
        5*pi*z**3/512 - 175*pi*z**4/32768 - 441*pi*z**5/131072 + O(z**6)
    assert E(4*z/(z+1)).series(z) == \
        pi/2 - pi*z/2 + pi*z**2/8 - 3*pi*z**3/8 - 15*pi*z**4/128 - 93*pi*z**5/128 + O(z**6)

    assert E(z, m).rewrite(Integral).dummy_eq(
        Integral(sqrt(1 - m*sin(t)**2), (t, 0, z)))
    assert E(m).rewrite(Integral).dummy_eq(
        Integral(sqrt(1 - m*sin(t)**2), (t, 0, pi/2)))


def test_E():
    z = S.Exp1
    assert z.is_commutative is True
    assert z.is_integer is False
    assert z.is_rational is False
    assert z.is_algebraic is False
    assert z.is_transcendental is True
    assert z.is_real is True
    assert z.is_complex is True
    assert z.is_noninteger is True
    assert z.is_irrational is True
    assert z.is_imaginary is False
    assert z.is_positive is True
    assert z.is_negative is False
    assert z.is_nonpositive is False
    assert z.is_nonnegative is True
    assert z.is_even is False
    assert z.is_odd is False
    assert z.is_finite is True
    assert z.is_infinite is False
    assert z.is_comparable is True
    assert z.is_prime is False
    assert z.is_composite is False


def test_E():
    z = S.Exp1
    assert ask(Q.commutative(z)) is True
    assert ask(Q.integer(z)) is False
    assert ask(Q.rational(z)) is False
    assert ask(Q.algebraic(z)) is False
    assert ask(Q.real(z)) is True
    assert ask(Q.complex(z)) is True
    assert ask(Q.irrational(z)) is True
    assert ask(Q.imaginary(z)) is False
    assert ask(Q.positive(z)) is True
    assert ask(Q.negative(z)) is False
    assert ask(Q.even(z)) is False
    assert ask(Q.odd(z)) is False
    assert ask(Q.finite(z)) is True
    assert ask(Q.prime(z)) is False
    assert ask(Q.composite(z)) is False
    assert ask(Q.hermitian(z)) is True
    assert ask(Q.antihermitian(z)) is False

