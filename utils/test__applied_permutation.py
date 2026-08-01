
def test_AppliedPermutation():
    p = Permutation(0, 1, 2)
    x = Symbol('x')
    assert latex(AppliedPermutation(p, x)) == \
        r'\sigma_{\left( 0\; 1\; 2\right)}(x)'


def test_AppliedPermutation():
    x = Symbol('x')
    p = Permutation(0, 1, 2)
    raises(ValueError, lambda: AppliedPermutation((0, 1, 2), x))
    assert AppliedPermutation(p, 1, evaluate=True) == 2
    assert AppliedPermutation(p, 1, evaluate=False).__class__ == \
        AppliedPermutation

