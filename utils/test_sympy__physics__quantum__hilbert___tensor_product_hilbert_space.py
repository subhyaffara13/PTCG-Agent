
def test_sympy__physics__quantum__hilbert__TensorProductHilbertSpace():
    from sympy.physics.quantum.hilbert import TensorProductHilbertSpace, FockSpace, ComplexSpace
    c = ComplexSpace(2)
    f = FockSpace()
    assert _test_args(TensorProductHilbertSpace(f, c))

