
def test_multi_norm_call_clip_inverse():
    # test get vmin, vmax
    norm = mpl.colors.MultiNorm(['linear', 'log'])
    norm.vmin = (1, 1)
    norm.vmax = (2, 2)

    # test call with clip
    assert_array_equal(norm([3, 3], clip=[False, False]), [2.0, 1.584962500721156])
    assert_array_equal(norm([3, 3], clip=[True, True]), [1.0, 1.0])
    assert_array_equal(norm([3, 3], clip=[True, False]), [1.0, 1.584962500721156])
    norm.clip = [False, False]
    assert_array_equal(norm([3, 3]), [2.0, 1.584962500721156])
    norm.clip = [True, True]
    assert_array_equal(norm([3, 3]), [1.0, 1.0])
    norm.clip = [True, False]
    assert_array_equal(norm([3, 3]), [1.0, 1.584962500721156])
    norm.clip = [True, True]

    with pytest.raises(ValueError, match="Expected an iterable of length 2"):
        norm.clip = True
    with pytest.raises(ValueError, match="Expected an iterable of length 2"):
        norm.clip = [True, False, True]
    with pytest.raises(ValueError, match="Expected an iterable of length 2"):
        norm([3, 3], clip=True)
    with pytest.raises(ValueError, match="Expected an iterable of length 2"):
        norm([3, 3], clip=[True, True, True])

    # test inverse
    assert_array_almost_equal(norm.inverse([0.5, 0.5849625007211562]), [1.5, 1.5])

