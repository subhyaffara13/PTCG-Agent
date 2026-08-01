
def test_sympy__tensor__tensor__TensorIndexType():
    from sympy.tensor.tensor import TensorIndexType
    assert _test_args(TensorIndexType('Lorentz'))

