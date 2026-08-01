
def test_scaled_zero():
    a, b = (([0], 1, 100, 1), -1)
    assert scaled_zero(100) == (a, b)
    assert scaled_zero(a) == (0, 1, 100, 1)
    a, b = (([1], 1, 100, 1), -1)
    assert scaled_zero(100, -1) == (a, b)
    assert scaled_zero(a) == (1, 1, 100, 1)
    raises(ValueError, lambda: scaled_zero(scaled_zero(100)))
    raises(ValueError, lambda: scaled_zero(100, 2))
    raises(ValueError, lambda: scaled_zero(100, 0))
    raises(ValueError, lambda: scaled_zero((1, 5, 1, 3)))

