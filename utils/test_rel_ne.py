
def test_rel_ne():
    assert Relational(x, y, '!=') == Ne(x, y)

    # issue 6116
    p = Symbol('p', positive=True)
    assert Ne(p, 0) is S.true

