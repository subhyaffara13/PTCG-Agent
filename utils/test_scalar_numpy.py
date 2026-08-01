
def test_scalar_numpy():
    if not np:
        skip("numpy not installed.")

    assert represent(Integer(1), format='numpy') == 1
    assert represent(Float(1.0), format='numpy') == 1.0
    assert represent(1.0 + I, format='numpy') == 1.0 + 1.0j

