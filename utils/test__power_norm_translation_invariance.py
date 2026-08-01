
def test_PowerNorm_translation_invariance():
    a = np.array([0, 1/2, 1], dtype=float)
    expected = [0, 1/8, 1]
    pnorm = mcolors.PowerNorm(vmin=0, vmax=1, gamma=3)
    assert_array_almost_equal(pnorm(a), expected)
    pnorm = mcolors.PowerNorm(vmin=-2, vmax=-1, gamma=3)
    assert_array_almost_equal(pnorm(a - 2), expected)

