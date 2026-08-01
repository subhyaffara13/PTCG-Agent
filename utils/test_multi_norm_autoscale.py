
def test_multi_norm_autoscale():
    norm = mpl.colors.MultiNorm(['linear', 'log'])
    # test autoscale
    norm.autoscale([[0, 1, 2, 3], [0.1, 1, 2, 3]])
    assert_array_equal(norm.vmin, [0, 0.1])
    assert_array_equal(norm.vmax, [3, 3])

    # test autoscale_none
    norm0 = mcolors.TwoSlopeNorm(2, vmin=0, vmax=None)
    norm = mcolors.MultiNorm([norm0, 'linear'], vmax=[None, 50])
    norm.autoscale_None([[1, 2, 3, 4, 5], [-50, 1, 0, 1, 500]])
    assert_array_equal(norm([5, 0]), [1, 0.5])
    assert_array_equal(norm.vmin, (0, -50))
    assert_array_equal(norm.vmax, (5, 50))

