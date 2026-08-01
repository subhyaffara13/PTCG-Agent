
def test_subs_iter():
    assert x.subs(reversed([[x, y]])) == y
    it = iter([[x, y]])
    assert x.subs(it) == y
    assert x.subs(Tuple((x, y))) == y

