
def test_atomic():
    g, h = map(Function, 'gh')
    x = symbols('x')
    assert _atomic(g(x + h(x))) == {g(x + h(x))}
    assert _atomic(g(x + h(x)), recursive=True) == {h(x), x, g(x + h(x))}
    assert _atomic(1) == set()
    assert _atomic(Basic(S(1), S(2))) == set()

