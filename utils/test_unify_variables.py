
def test_unify_variables():
    assert list(unify(Basic(S(1), S(2)), Basic(S(1), x), {}, variables=(x,))) == [{x: 2}]

