
def test_sympy__functions__special__hyper__hyper():
    from sympy.functions.special.hyper import hyper
    assert _test_args(hyper([1, 2, 3], [4, 5], x))

