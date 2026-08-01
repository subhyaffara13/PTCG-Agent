
def test_twinx_cla():
    fig, ax = plt.subplots()
    ax2 = ax.twinx()
    ax3 = ax2.twiny()
    plt.draw()
    assert not ax2.xaxis.get_visible()
    assert not ax2.patch.get_visible()
    ax2.cla()
    ax3.cla()

    assert not ax2.xaxis.get_visible()
    assert not ax2.patch.get_visible()
    assert ax2.yaxis.get_visible()

    assert ax3.xaxis.get_visible()
    assert not ax3.patch.get_visible()
    assert not ax3.yaxis.get_visible()

    assert ax.xaxis.get_visible()
    assert ax.patch.get_visible()
    assert ax.yaxis.get_visible()

