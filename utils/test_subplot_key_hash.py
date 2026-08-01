
def test_subplot_key_hash():
    ax = plt.subplot(np.int32(5), np.int64(1), 1)
    ax.twinx()
    assert ax.get_subplotspec().get_geometry() == (5, 1, 0, 0)

