
def test_sympy__tensor__tensor__WildTensorHead():
    from sympy.tensor.tensor import WildTensorHead
    assert _test_args(WildTensorHead('p'))

