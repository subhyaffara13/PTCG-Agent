
def test_sympy__tensor__toperators__PartialDerivative():
    from sympy.tensor.tensor import TensorIndexType, tensor_indices, TensorHead
    from sympy.tensor.toperators import PartialDerivative
    Lorentz = TensorIndexType('Lorentz', dummy_name='L')
    a, b = tensor_indices('a,b', Lorentz)
    A = TensorHead("A", [Lorentz])
    assert _test_args(PartialDerivative(A(a), A(b)))

