
def test_associative():
    c1 = C('Add', (1,2,3))
    c2 = C('Add', (x,y))
    assert tuple(unify(c1, c2, {})) == ({x: 1, y: C('Add', (2, 3))},
                                         {x: C('Add', (1, 2)), y: 3})

