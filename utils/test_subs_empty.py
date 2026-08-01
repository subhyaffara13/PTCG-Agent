
def test_subs_empty():
    assert subs({})(Basic(S(1), S(2))) == Basic(S(1), S(2))

