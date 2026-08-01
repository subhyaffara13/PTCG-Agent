
def test_sympy__tensor__tensor__TensorHead():
    from sympy.tensor.tensor import TensorIndexType, TensorSymmetry, get_symmetric_group_sgs, TensorHead
    Lorentz = TensorIndexType('Lorentz', dummy_name='L')
    sym = TensorSymmetry(get_symmetric_group_sgs(1))
    assert _test_args(TensorHead('p', [Lorentz], sym, 0))

