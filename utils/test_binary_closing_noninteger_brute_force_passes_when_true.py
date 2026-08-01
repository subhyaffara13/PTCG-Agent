
def test_binary_closing_noninteger_brute_force_passes_when_true(xp):
    # regression test for gh-9905, gh-9909: ValueError for non integer iterations
    data = xp.ones([1])
    xp_assert_equal(ndimage.binary_erosion(data, iterations=2, brute_force=1.5),
                    ndimage.binary_erosion(data, iterations=2, brute_force=bool(1.5))
    )
    xp_assert_equal(ndimage.binary_erosion(data, iterations=2, brute_force=0.0),
                    ndimage.binary_erosion(data, iterations=2, brute_force=bool(0.0))
    )

