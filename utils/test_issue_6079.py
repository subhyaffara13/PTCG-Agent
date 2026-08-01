
def test_issue_6079():
    # since x + 2.0 == x + 2 we can't do a simple equality test
    assert _aresame((x + 2.0).subs(2, 3), x + 2.0)
    assert _aresame((x + 2.0).subs(2.0, 3), x + 3)
    assert not _aresame(x + 2, x + 2.0)
    assert not _aresame(Basic(cos(x), S(1)), Basic(cos(x), S(1.)))
    assert _aresame(cos, cos)
    assert not _aresame(1, S.One)
    assert not _aresame(x, symbols('x', positive=True))

