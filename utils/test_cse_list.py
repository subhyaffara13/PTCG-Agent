
def test_cse_list():
    _cse = lambda x: cse(x, list=False)
    assert _cse(x) == ([], x)
    assert _cse('x') == ([], 'x')
    it = [x]
    for c in (list, tuple, set):
        assert _cse(c(it)) == ([], c(it))
    #Tuple works different from tuple:
    assert _cse(Tuple(*it)) == ([], Tuple(*it))
    d = {x: 1}
    assert _cse(d) == ([], d)

