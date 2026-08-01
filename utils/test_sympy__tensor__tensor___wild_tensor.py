
def test_sympy__tensor__tensor__WildTensor():
    from sympy.tensor.tensor import TensorIndexType, WildTensorHead, TensorIndex
    Lorentz = TensorIndexType('Lorentz', dummy_name='L')
    a = TensorIndex('a', Lorentz)
    p = WildTensorHead('p')
    assert _test_args(p(a))

