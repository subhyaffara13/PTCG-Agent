
def test_interface():
    x, y = map(Symbol, 'xy')
    p, q = map(Wild, 'pq')

    assert (x + 1).match(p + 1) == {p: x}
    assert (x*3).match(p*3) == {p: x}
    assert (x**3).match(p**3) == {p: x}
    assert (x*cos(y)).match(p*cos(q)) == {p: x, q: y}

    assert (x*y).match(p*q) in [{p:x, q:y}, {p:y, q:x}]
    assert (x + y).match(p + q) in [{p:x, q:y}, {p:y, q:x}]
    assert (x*y + 1).match(p*q) in [{p:1, q:1 + x*y}, {p:1 + x*y, q:1}]

