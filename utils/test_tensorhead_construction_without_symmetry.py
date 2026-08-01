
def test_tensorhead_construction_without_symmetry():
    L = TensorIndexType('Lorentz')
    A1 = TensorHead('A', [L, L])
    A2 = TensorHead('A', [L, L], TensorSymmetry.no_symmetry(2))
    assert A1 == A2
    A3 = TensorHead('A', [L, L], TensorSymmetry.fully_symmetric(2))  # Symmetric
    assert A1 != A3

