
def test_sympy__tensor__tensor__WildTensorIndex():
    from sympy.tensor.tensor import TensorIndexType, WildTensorIndex
    Lorentz = TensorIndexType('Lorentz', dummy_name='L')
    assert _test_args(WildTensorIndex('i', Lorentz))

