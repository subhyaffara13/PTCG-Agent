
def test_scalar_scipy_sparse():
    if not np:
        skip("numpy not installed.")
    if not scipy:
        skip("scipy not installed.")

    assert represent(Integer(1), format='scipy.sparse') == 1
    assert represent(Float(1.0), format='scipy.sparse') == 1.0
    assert represent(1.0 + I, format='scipy.sparse') == 1.0 + 1.0j

