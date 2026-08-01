
def test_Dict():
    assert str(Dict({1: 1 + x})) == sstr({1: 1 + x}) == "{1: x + 1}"
    assert str(Dict({1: x**2, 2: y*x})) in (
        "{1: x**2, 2: x*y}", "{2: x*y, 1: x**2}")
    assert sstr(Dict({1: x**2, 2: y*x})) == "{1: x**2, 2: x*y}"


def test_Dict():
    x, y, z = symbols('x y z')
    d = Dict({x: 1, y: 2, z: 3})
    assert d[x] == 1
    assert d[y] == 2
    raises(KeyError, lambda: d[2])
    raises(KeyError, lambda: d['2'])
    assert len(d) == 3
    assert set(d.keys()) == {x, y, z}
    assert set(d.values()) == {S.One, S(2), S(3)}
    assert d.get(5, 'default') == 'default'
    assert d.get('5', 'default') == 'default'
    assert x in d and z in d and 5 not in d and '5' not in d
    assert d.has(x) and d.has(1)  # SymPy Basic .has method

    # Test input types
    # input - a Python dict
    # input - items as args - SymPy style
    assert (Dict({x: 1, y: 2, z: 3}) ==
            Dict((x, 1), (y, 2), (z, 3)))

    raises(TypeError, lambda: Dict(((x, 1), (y, 2), (z, 3))))
    with raises(NotImplementedError):
        d[5] = 6  # assert immutability

    assert set(
        d.items()) == {Tuple(x, S.One), Tuple(y, S(2)), Tuple(z, S(3))}
    assert set(d) == {x, y, z}
    assert str(d) == '{x: 1, y: 2, z: 3}'
    assert d.__repr__() == '{x: 1, y: 2, z: 3}'

    # Test creating a Dict from a Dict.
    d = Dict({x: 1, y: 2, z: 3})
    assert d == Dict(d)

    # Test for supporting defaultdict
    d = defaultdict(int)
    assert d[x] == 0
    assert d[y] == 0
    assert d[z] == 0
    assert Dict(d)
    d = Dict(d)
    assert len(d) == 3
    assert set(d.keys()) == {x, y, z}
    assert set(d.values()) == {S.Zero, S.Zero, S.Zero}

