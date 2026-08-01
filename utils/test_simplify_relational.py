
def test_simplify_relational():
    assert simplify(x*(y + 1) - x*y - x + 1 < x) == (x > 1)
    assert simplify(x*(y + 1) - x*y - x - 1 < x) == (x > -1)
    assert simplify(x < x*(y + 1) - x*y - x + 1) == (x < 1)
    q, r = symbols("q r")
    assert (((-q + r) - (q - r)) <= 0).simplify() == (q >= r)
    root2 = sqrt(2)
    equation = ((root2 * (-q + r) - root2 * (q - r)) <= 0).simplify()
    assert equation == (q >= r)
    r = S.One < x
    # canonical operations are not the same as simplification,
    # so if there is no simplification, canonicalization will
    # be done unless the measure forbids it
    assert simplify(r) == r.canonical
    assert simplify(r, ratio=0) != r.canonical
    # this is not a random test; in _eval_simplify
    # this will simplify to S.false and that is the
    # reason for the 'if r.is_Relational' in Relational's
    # _eval_simplify routine
    assert simplify(-(2**(pi*Rational(3, 2)) + 6**pi)**(1/pi) +
                    2*(2**(pi/2) + 3**pi)**(1/pi) < 0) is S.false
    # canonical at least
    assert Eq(y, x).simplify() == Eq(x, y)
    assert Eq(x - 1, 0).simplify() == Eq(x, 1)
    assert Eq(x - 1, x).simplify() == S.false
    assert Eq(2*x - 1, x).simplify() == Eq(x, 1)
    assert Eq(2*x, 4).simplify() == Eq(x, 2)
    z = cos(1)**2 + sin(1)**2 - 1  # z.is_zero is None
    assert Eq(z*x, 0).simplify() == S.true

    assert Ne(y, x).simplify() == Ne(x, y)
    assert Ne(x - 1, 0).simplify() == Ne(x, 1)
    assert Ne(x - 1, x).simplify() == S.true
    assert Ne(2*x - 1, x).simplify() == Ne(x, 1)
    assert Ne(2*x, 4).simplify() == Ne(x, 2)
    assert Ne(z*x, 0).simplify() == S.false

    # No real-valued assumptions
    assert Ge(y, x).simplify() == Le(x, y)
    assert Ge(x - 1, 0).simplify() == Ge(x, 1)
    assert Ge(x - 1, x).simplify() == S.false
    assert Ge(2*x - 1, x).simplify() == Ge(x, 1)
    assert Ge(2*x, 4).simplify() == Ge(x, 2)
    assert Ge(z*x, 0).simplify() == S.true
    assert Ge(x, -2).simplify() == Ge(x, -2)
    assert Ge(-x, -2).simplify() == Le(x, 2)
    assert Ge(x, 2).simplify() == Ge(x, 2)
    assert Ge(-x, 2).simplify() == Le(x, -2)

    assert Le(y, x).simplify() == Ge(x, y)
    assert Le(x - 1, 0).simplify() == Le(x, 1)
    assert Le(x - 1, x).simplify() == S.true
    assert Le(2*x - 1, x).simplify() == Le(x, 1)
    assert Le(2*x, 4).simplify() == Le(x, 2)
    assert Le(z*x, 0).simplify() == S.true
    assert Le(x, -2).simplify() == Le(x, -2)
    assert Le(-x, -2).simplify() == Ge(x, 2)
    assert Le(x, 2).simplify() == Le(x, 2)
    assert Le(-x, 2).simplify() == Ge(x, -2)

    assert Gt(y, x).simplify() == Lt(x, y)
    assert Gt(x - 1, 0).simplify() == Gt(x, 1)
    assert Gt(x - 1, x).simplify() == S.false
    assert Gt(2*x - 1, x).simplify() == Gt(x, 1)
    assert Gt(2*x, 4).simplify() == Gt(x, 2)
    assert Gt(z*x, 0).simplify() == S.false
    assert Gt(x, -2).simplify() == Gt(x, -2)
    assert Gt(-x, -2).simplify() == Lt(x, 2)
    assert Gt(x, 2).simplify() == Gt(x, 2)
    assert Gt(-x, 2).simplify() == Lt(x, -2)

    assert Lt(y, x).simplify() == Gt(x, y)
    assert Lt(x - 1, 0).simplify() == Lt(x, 1)
    assert Lt(x - 1, x).simplify() == S.true
    assert Lt(2*x - 1, x).simplify() == Lt(x, 1)
    assert Lt(2*x, 4).simplify() == Lt(x, 2)
    assert Lt(z*x, 0).simplify() == S.false
    assert Lt(x, -2).simplify() == Lt(x, -2)
    assert Lt(-x, -2).simplify() == Gt(x, 2)
    assert Lt(x, 2).simplify() == Lt(x, 2)
    assert Lt(-x, 2).simplify() == Gt(x, -2)

    # Test particular branches of _eval_simplify
    m = exp(1) - exp_polar(1)
    assert simplify(m*x > 1) is S.false
    # These two test the same branch
    assert simplify(m*x + 2*m*y > 1) is S.false
    assert simplify(m*x + y > 1 + y) is S.false

