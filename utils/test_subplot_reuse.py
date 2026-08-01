
def test_subplot_reuse():
    ax1 = plt.subplot(121)
    assert ax1 is plt.gca()
    ax2 = plt.subplot(122)
    assert ax2 is plt.gca()
    ax3 = plt.subplot(121)
    assert ax1 is plt.gca()
    assert ax1 is ax3

