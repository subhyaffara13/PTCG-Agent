
def test_hist_zorder(histtype, zorder):
    ax = plt.figure().add_subplot()
    ax.hist([1, 2], histtype=histtype)
    assert ax.patches
    for patch in ax.patches:
        assert patch.get_zorder() == zorder

