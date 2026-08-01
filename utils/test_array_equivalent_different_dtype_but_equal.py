
def test_array_equivalent_different_dtype_but_equal():
    # Unclear if this is exposed anywhere in the public-facing API
    assert array_equivalent(np.array([1, 2]), np.array([1.0, 2.0]))

