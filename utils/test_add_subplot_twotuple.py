
def test_add_subplot_twotuple():
    fig = plt.figure()
    ax1 = fig.add_subplot(3, 2, (3, 5))
    assert ax1.get_subplotspec().rowspan == range(1, 3)
    assert ax1.get_subplotspec().colspan == range(0, 1)
    ax2 = fig.add_subplot(3, 2, (4, 6))
    assert ax2.get_subplotspec().rowspan == range(1, 3)
    assert ax2.get_subplotspec().colspan == range(1, 2)
    ax3 = fig.add_subplot(3, 2, (3, 6))
    assert ax3.get_subplotspec().rowspan == range(1, 3)
    assert ax3.get_subplotspec().colspan == range(0, 2)
    ax4 = fig.add_subplot(3, 2, (4, 5))
    assert ax4.get_subplotspec().rowspan == range(1, 3)
    assert ax4.get_subplotspec().colspan == range(0, 2)
    with pytest.raises(IndexError):
        fig.add_subplot(3, 2, (6, 3))

