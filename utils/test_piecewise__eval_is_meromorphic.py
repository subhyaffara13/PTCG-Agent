
def test_piecewise__eval_is_meromorphic():
    """ Issue 24127: Tests eval_is_meromorphic auxiliary method """
    x = symbols('x', real=True)
    f = Piecewise((1, x < 0), (sqrt(1 - x), True))
    assert f.is_meromorphic(x, I) is None
    assert f.is_meromorphic(x, -1) == True
    assert f.is_meromorphic(x, 0) == None
    assert f.is_meromorphic(x, 1) == False
    assert f.is_meromorphic(x, 2) == True
    assert f.is_meromorphic(x, Symbol('a')) == None
    assert f.is_meromorphic(x, Symbol('a', real=True)) == None

