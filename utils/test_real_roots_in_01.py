
def test_real_roots_in_01(roots, expected_in_01):
    roots = np.array(roots)
    coeffs = np.poly(roots)[::-1]  # np.poly gives descending, we need ascending
    result = _real_roots_in_01(coeffs.real)
    assert_allclose(result, expected_in_01, atol=1e-10)

