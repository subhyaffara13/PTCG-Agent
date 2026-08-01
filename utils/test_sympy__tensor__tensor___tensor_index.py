
def test_sympy__tensor__tensor__TensorIndex():
    from sympy.tensor.tensor import TensorIndexType, TensorIndex
    Lorentz = TensorIndexType('Lorentz', dummy_name='L')
    assert _test_args(TensorIndex('i', Lorentz))

