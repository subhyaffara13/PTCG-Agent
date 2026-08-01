
def test_TwoSlopeNorm_Even():
    norm = mcolors.TwoSlopeNorm(vmin=-1, vcenter=0, vmax=4)
    vals = np.array([-1.0, -0.5, 0.0, 1.0, 2.0, 3.0, 4.0])
    expected = np.array([0.0, 0.25, 0.5, 0.625, 0.75, 0.875, 1.0])
    assert_array_equal(norm(vals), expected)

