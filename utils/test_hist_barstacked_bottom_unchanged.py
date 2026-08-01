
def test_hist_barstacked_bottom_unchanged():
    b = np.array([10, 20])
    plt.hist([[0, 1], [0, 1]], 2, histtype="barstacked", bottom=b)
    assert b.tolist() == [10, 20]

