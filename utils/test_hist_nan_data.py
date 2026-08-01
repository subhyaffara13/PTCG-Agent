
def test_hist_nan_data():
    fig, (ax1, ax2) = plt.subplots(2)

    data = [1, 2, 3]
    nan_data = data + [np.nan]

    bins, edges, _ = ax1.hist(data)
    with np.errstate(invalid='ignore'):
        nanbins, nanedges, _ = ax2.hist(nan_data)

    np.testing.assert_allclose(bins, nanbins)
    np.testing.assert_allclose(edges, nanedges)

