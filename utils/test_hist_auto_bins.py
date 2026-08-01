
def test_hist_auto_bins():
    _, bins, _ = plt.hist([[1, 2, 3], [3, 4, 5, 6]], bins='auto')
    assert bins[0] <= 1
    assert bins[-1] >= 6

