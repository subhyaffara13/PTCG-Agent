
def test_PowerNorm():
    # Check an exponent of 1 gives same results as a normal linear
    # normalization. Also implicitly checks that vmin/vmax are
    # automatically initialized from first array input.
    a = np.array([0, 0.5, 1, 1.5], dtype=float)
    pnorm = mcolors.PowerNorm(1)
    norm = mcolors.Normalize()
    assert_array_almost_equal(norm(a), pnorm(a))

    a = np.array([-0.5, 0, 2, 4, 8], dtype=float)
    expected = [-1/16, 0, 1/16, 1/4, 1]
    pnorm = mcolors.PowerNorm(2, vmin=0, vmax=8)
    assert_array_almost_equal(pnorm(a), expected)
    assert pnorm(a[0]) == expected[0]
    assert pnorm(a[2]) == expected[2]
    # Check inverse
    a_roundtrip = pnorm.inverse(pnorm(a))
    assert_array_almost_equal(a, a_roundtrip)
    # PowerNorm inverse adds a mask, so check that is correct too
    assert_array_equal(a_roundtrip.mask, np.zeros(a.shape, dtype=bool))

    # Clip = True
    a = np.array([-0.5, 0, 1, 8, 16], dtype=float)
    expected = [0, 0, 0, 1, 1]
    # Clip = True when creating the norm
    pnorm = mcolors.PowerNorm(2, vmin=2, vmax=8, clip=True)
    assert_array_almost_equal(pnorm(a), expected)
    assert pnorm(a[0]) == expected[0]
    assert pnorm(a[-1]) == expected[-1]
    # Clip = True at call time
    pnorm = mcolors.PowerNorm(2, vmin=2, vmax=8, clip=False)
    assert_array_almost_equal(pnorm(a, clip=True), expected)
    assert pnorm(a[0], clip=True) == expected[0]
    assert pnorm(a[-1], clip=True) == expected[-1]

    # Check clip=True preserves masked values
    a = np.ma.array([5, 2], mask=[True, False])
    out = pnorm(a, clip=True)
    assert_array_equal(out.mask, [True, False])

