
def test_sen_seasonal_slopes():
    rng = np.random.default_rng(5765986256978575148)
    x = rng.random(size=(100, 4))
    intra_slope, inter_slope = mstats.sen_seasonal_slopes(x)

    # reference implementation from the `sen_seasonal_slopes` documentation
    def dijk(yi):
        n = len(yi)
        x = np.arange(n)
        dy = yi - yi[:, np.newaxis]
        dx = x - x[:, np.newaxis]
        mask = np.triu(np.ones((n, n), dtype=bool), k=1)
        return dy[mask]/dx[mask]

    for i in range(4):
        assert_allclose(np.median(dijk(x[:, i])), intra_slope[i])

    all_slopes = np.concatenate([dijk(x[:, i]) for i in range(x.shape[1])])
    assert_allclose(np.median(all_slopes), inter_slope)

