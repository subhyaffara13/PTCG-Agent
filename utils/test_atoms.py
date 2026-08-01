
def test_atoms():
    # Non-Symbol atoms should not be pulled out from the expression namespace
    f = lambdify(x, pi + x, {"pi": 3.14})
    assert f(0) == 3.14
    f = lambdify(x, I + x, {"I": 1j})
    assert f(1) == 1 + 1j


def test_atoms():
    m = PropertiesOnlyMatrix(2, 2, [1, 2, x, 1 - 1/x])
    assert m.atoms() == {S.One, S(2), S.NegativeOne, x}
    assert m.atoms(Symbol) == {x}


def test_atoms():
    m = Matrix([[1, 2], [x, 1 - 1/x]])
    assert m.atoms() == {S.One,S(2),S.NegativeOne, x}
    assert m.atoms(Symbol) == {x}


def test_atoms():
    m = Matrix([[1, 2], [x, 1 - 1/x]])
    assert m.atoms() == {S.One,S(2),S.NegativeOne, x}
    assert m.atoms(Symbol) == {x}


def test_atoms():
    assert b21.atoms() == {Basic()}


def test_atoms():
    assert x.atoms() == {x}
    assert (1 + x).atoms() == {x, S.One}

    assert (1 + 2*cos(x)).atoms(Symbol) == {x}
    assert (1 + 2*cos(x)).atoms(Symbol, Number) == {S.One, S(2), x}

    assert (2*(x**(y**x))).atoms() == {S(2), x, y}

    assert S.Half.atoms() == {S.Half}
    assert S.Half.atoms(Symbol) == set()

    assert sin(oo).atoms(oo) == set()

    assert Poly(0, x).atoms() == {S.Zero, x}
    assert Poly(1, x).atoms() == {S.One, x}

    assert Poly(x, x).atoms() == {x}
    assert Poly(x, x, y).atoms() == {x, y}
    assert Poly(x + y, x, y).atoms() == {x, y}
    assert Poly(x + y, x, y, z).atoms() == {x, y, z}
    assert Poly(x + y*t, x, y, z).atoms() == {t, x, y, z}

    assert (I*pi).atoms(NumberSymbol) == {pi}
    assert (I*pi).atoms(NumberSymbol, I) == \
        (I*pi).atoms(I, NumberSymbol) == {pi, I}

    assert exp(exp(x)).atoms(exp) == {exp(exp(x)), exp(x)}
    assert (1 + x*(2 + y) + exp(3 + z)).atoms(Add) == \
        {1 + x*(2 + y) + exp(3 + z), 2 + y, 3 + z}

    # issue 6132
    e = (f(x) + sin(x) + 2)
    assert e.atoms(AppliedUndef) == \
        {f(x)}
    assert e.atoms(AppliedUndef, Function) == \
        {f(x), sin(x)}
    assert e.atoms(Function) == \
        {f(x), sin(x)}
    assert e.atoms(AppliedUndef, Number) == \
        {f(x), S(2)}
    assert e.atoms(Function, Number) == \
        {S(2), sin(x), f(x)}

