
def test_denoms():
    assert denoms(x/2 + 1/y) == {2, y}
    assert denoms(x/2 + 1/y, y) == {y}
    assert denoms(x/2 + 1/y, [y]) == {y}
    assert denoms(1/x + 1/y + 1/z, [x, y]) == {x, y}
    assert denoms(1/x + 1/y + 1/z, x, y) == {x, y}
    assert denoms(1/x + 1/y + 1/z, {x, y}) == {x, y}

