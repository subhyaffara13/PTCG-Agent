
def test_odd_query():
    assert ask(Q.odd(x)) is None
    assert ask(Q.odd(x), Q.odd(x)) is True
    assert ask(Q.odd(x), Q.integer(x)) is None
    assert ask(Q.odd(x), ~Q.integer(x)) is False
    assert ask(Q.odd(x), Q.rational(x)) is None
    assert ask(Q.odd(x), Q.positive(x)) is None

    assert ask(Q.odd(-x), Q.odd(x)) is True

    assert ask(Q.odd(2*x)) is None
    assert ask(Q.odd(2*x), Q.integer(x)) is False
    assert ask(Q.odd(2*x), Q.odd(x)) is False
    assert ask(Q.odd(2*x), Q.irrational(x)) is False
    assert ask(Q.odd(2*x), ~Q.integer(x)) is None
    assert ask(Q.odd(3*x), Q.integer(x)) is None

    assert ask(Q.odd(x/3), Q.odd(x)) is None
    assert ask(Q.odd(x/3), Q.even(x)) is None

    assert ask(Q.odd(x + 1), Q.even(x)) is True
    assert ask(Q.odd(x + 2), Q.even(x)) is False
    assert ask(Q.odd(x + 2), Q.odd(x)) is True
    assert ask(Q.odd(3 - x), Q.odd(x)) is False
    assert ask(Q.odd(3 - x), Q.even(x)) is True
    assert ask(Q.odd(3 + x), Q.odd(x)) is False
    assert ask(Q.odd(3 + x), Q.even(x)) is True
    assert ask(Q.odd(x + y), Q.odd(x) & Q.odd(y)) is False
    assert ask(Q.odd(x + y), Q.odd(x) & Q.even(y)) is True
    assert ask(Q.odd(x - y), Q.even(x) & Q.odd(y)) is True
    assert ask(Q.odd(x - y), Q.odd(x) & Q.odd(y)) is False

    assert ask(Q.odd(x + y + z), Q.odd(x) & Q.odd(y) & Q.even(z)) is False
    assert ask(Q.odd(x + y + z + t),
        Q.odd(x) & Q.odd(y) & Q.even(z) & Q.integer(t)) is None

    assert ask(Q.odd(2*x + 1), Q.integer(x)) is True
    assert ask(Q.odd(2*x + y), Q.integer(x) & Q.odd(y)) is True
    assert ask(Q.odd(2*x + y), Q.integer(x) & Q.even(y)) is False
    assert ask(Q.odd(2*x + y), Q.integer(x) & Q.integer(y)) is None
    assert ask(Q.odd(x*y), Q.odd(x) & Q.even(y)) is False
    assert ask(Q.odd(x*y), Q.odd(x) & Q.odd(y)) is True
    assert ask(Q.odd(2*x*y), Q.rational(x) & Q.rational(x)) is None
    assert ask(Q.odd(2*x*y), Q.irrational(x) & Q.irrational(x)) is None

    assert ask(Q.odd(Abs(x)), Q.odd(x)) is True

    assert ask(Q.odd((-1)**n), Q.integer(n)) is True

    assert ask(Q.odd(k**2), Q.even(k)) is False
    assert ask(Q.odd(n**2), Q.odd(n)) is True
    assert ask(Q.odd(3**k), Q.even(k)) is None

    assert ask(Q.odd(k**m), Q.even(k) & Q.integer(m) & ~Q.negative(m)) is None
    assert ask(Q.odd(n**m), Q.odd(n) & Q.integer(m) & ~Q.negative(m)) is True

    assert ask(Q.odd(k**p), Q.even(k) & Q.integer(p) & Q.positive(p)) is False
    assert ask(Q.odd(n**p), Q.odd(n) & Q.integer(p) & Q.positive(p)) is True

    assert ask(Q.odd(m**k), Q.even(k) & Q.integer(m) & ~Q.negative(m)) is None
    assert ask(Q.odd(p**k), Q.even(k) & Q.integer(p) & Q.positive(p)) is None

    assert ask(Q.odd(m**n), Q.odd(n) & Q.integer(m) & ~Q.negative(m)) is None
    assert ask(Q.odd(p**n), Q.odd(n) & Q.integer(p) & Q.positive(p)) is None

    assert ask(Q.odd(k**x), Q.even(k)) is None
    assert ask(Q.odd(n**x), Q.odd(n)) is None

    assert ask(Q.odd(x*y), Q.integer(x) & Q.integer(y)) is None
    assert ask(Q.odd(x*x), Q.integer(x)) is None
    assert ask(Q.odd(x*(x + y)), Q.integer(x) & Q.odd(y)) is False
    assert ask(Q.odd(x*(x + y)), Q.integer(x) & Q.even(y)) is None

