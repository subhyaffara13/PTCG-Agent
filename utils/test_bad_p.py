
def test_bad_p(p):
    # Raise ValueError if p <=0.
    with pytest.raises(ValueError):
        minkowski([1, 2], [3, 4], p)
    with pytest.raises(ValueError):
        minkowski([1, 2], [3, 4], p, [1, 1])

