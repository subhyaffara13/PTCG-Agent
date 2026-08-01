
def test_sympify_set():
    n = Symbol('n')
    assert sympify({n}) == FiniteSet(n)
    assert sympify(set()) == EmptySet

