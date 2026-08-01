
def test_mi_compute(values, expected):
    # Equivalent to unittest's assertAlmostEqual
    assert round(mi_compute(*values) - expected, 5) == 0

