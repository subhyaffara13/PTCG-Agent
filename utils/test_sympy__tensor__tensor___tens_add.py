
def test_sympy__tensor__tensor__TensAdd():
    from sympy.tensor.tensor import TensorIndexType, TensorSymmetry, get_symmetric_group_sgs, tensor_indices, TensAdd, tensor_heads
    Lorentz = TensorIndexType('Lorentz', dummy_name='L')
    a, b = tensor_indices('a,b', Lorentz)
    sym = TensorSymmetry(get_symmetric_group_sgs(1))
    p, q = tensor_heads('p,q', [Lorentz], sym)
    t1 = p(a)
    t2 = q(a)
    assert _test_args(TensAdd(t1, t2))

