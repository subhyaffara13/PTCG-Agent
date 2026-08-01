
def test_permutation_apply():
    x = Symbol('x')
    p = Permutation(0, 1, 2)
    assert p.apply(0) == 1
    assert isinstance(p.apply(0), Integer)
    assert p.apply(x) == AppliedPermutation(p, x)
    assert AppliedPermutation(p, x).subs(x, 0) == 1

    x = Symbol('x', integer=False)
    raises(NotImplementedError, lambda: p.apply(x))
    x = Symbol('x', negative=True)
    raises(NotImplementedError, lambda: p.apply(x))

