
def test_canonicalize3():
    D = Symbol('D')
    Spinor = TensorIndexType('Spinor', dim=D, metric_symmetry=-1, dummy_name='S')
    a0,a1,a2,a3,a4 = tensor_indices('a0:5', Spinor)
    chi, psi = tensor_heads('chi,psi', [Spinor], TensorSymmetry.no_symmetry(1), 1)

    t = chi(a1)*psi(a0)
    t1 = t.canon_bp()
    assert t1 == t

    t = psi(a1)*chi(a0)
    t1 = t.canon_bp()
    assert t1 == -chi(a0)*psi(a1)

