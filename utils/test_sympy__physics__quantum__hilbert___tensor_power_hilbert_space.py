
def test_sympy__physics__quantum__hilbert__TensorPowerHilbertSpace():
    from sympy.physics.quantum.hilbert import TensorPowerHilbertSpace, FockSpace
    f = FockSpace()
    assert _test_args(TensorPowerHilbertSpace(f, 2))

