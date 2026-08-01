
def test_sympy__physics__quantum__qft__IQFT():
    from sympy.physics.quantum.qft import IQFT
    assert _test_args(IQFT(0, 1))

