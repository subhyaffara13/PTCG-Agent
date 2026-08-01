
def test_sympy__tensor__tensor__TensMul():
    from sympy.tensor.tensor import TensorIndexType, TensorSymmetry, get_symmetric_group_sgs, tensor_indices, tensor_heads
    Lorentz = TensorIndexType('Lorentz', dummy_name='L')
    a, b = tensor_indices('a,b', Lorentz)
    sym = TensorSymmetry(get_symmetric_group_sgs(1))
    p, q = tensor_heads('p, q', [Lorentz], sym)
    assert _test_args(3*p(a)*q(b))

