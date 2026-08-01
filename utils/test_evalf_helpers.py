
def test_evalf_helpers():
    from mpmath.libmp import finf
    assert complex_accuracy((from_float(2.0), None, 35, None)) == 35
    assert complex_accuracy((from_float(2.0), from_float(10.0), 35, 100)) == 37
    assert complex_accuracy(
        (from_float(2.0), from_float(1000.0), 35, 100)) == 43
    assert complex_accuracy((from_float(2.0), from_float(10.0), 100, 35)) == 35
    assert complex_accuracy(
        (from_float(2.0), from_float(1000.0), 100, 35)) == 35
    assert complex_accuracy(finf) == math.inf
    assert complex_accuracy(zoo) == math.inf
    raises(ValueError, lambda: get_integer_part(zoo, 1, {}))

