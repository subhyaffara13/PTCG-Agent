
def test_sympy__tensor__tensor__Tensor():
    from sympy.tensor.tensor import TensorIndexType, TensorSymmetry, get_symmetric_group_sgs, tensor_indices, TensorHead
    Lorentz = TensorIndexType('Lorentz', dummy_name='L')
    a, b = tensor_indices('a,b', Lorentz)
    sym = TensorSymmetry(get_symmetric_group_sgs(1))
    p = TensorHead('p', [Lorentz], sym)
    assert _test_args(p(a))

