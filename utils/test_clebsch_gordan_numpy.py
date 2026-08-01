
def test_clebsch_gordan_numpy():
    try:
        import numpy as np
    except ImportError:
        skip("numpy not installed")
    assert clebsch_gordan(*np.zeros(6).astype(np.int64)) == 1
    assert wigner_3j(2, np.float64(6.0), 4.0, 0, 0, 0) == sqrt(715)/143
    assert wigner_3j(0, 0.5, 0.5, 0, 0.5, -0.5) == sqrt(2)/2
    raises(ValueError, lambda: wigner_3j(2.1, 6, 4, 0, 0, 0))

