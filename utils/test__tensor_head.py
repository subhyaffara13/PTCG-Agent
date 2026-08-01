
def test_TensorHead():
    # simple example of algebraic expression
    Lorentz = TensorIndexType('Lorentz', dummy_name='L')
    A = TensorHead('A', [Lorentz]*2)
    assert A.name == 'A'
    assert A.index_types == [Lorentz, Lorentz]
    assert A.rank == 2
    assert A.symmetry == TensorSymmetry.no_symmetry(2)
    assert A.comm == 0

