
def test_histogram_non_uniform():
    # Tests rv_histogram works even for non-uniform bin widths
    counts, bins = ([1, 1], [0, 1, 1001])

    dist = stats.rv_histogram((counts, bins), density=False)
    np.testing.assert_allclose(dist.pdf([0.5, 200]), [0.5, 0.0005])
    assert dist.median() == 1

    dist = stats.rv_histogram((counts, bins), density=True)
    np.testing.assert_allclose(dist.pdf([0.5, 200]), 1/1001)
    assert dist.median() == 1001/2

    # Omitting density produces a warning for non-uniform bins...
    message = "Bin widths are not constant. Assuming..."
    with pytest.warns(RuntimeWarning, match=message):
        dist = stats.rv_histogram((counts, bins))
        assert dist.median() == 1001/2  # default is like `density=True`

    # ... but not for uniform bins
    dist = stats.rv_histogram((counts, [0, 1, 2]))
    assert dist.median() == 1

