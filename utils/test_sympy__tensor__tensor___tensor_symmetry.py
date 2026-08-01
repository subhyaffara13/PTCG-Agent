
def test_sympy__tensor__tensor__TensorSymmetry():
    from sympy.tensor.tensor import TensorSymmetry, get_symmetric_group_sgs
    assert _test_args(TensorSymmetry(get_symmetric_group_sgs(2)))

