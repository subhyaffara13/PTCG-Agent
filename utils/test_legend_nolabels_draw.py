
def test_legend_nolabels_draw():
    plt.plot([1, 2, 3])
    plt.legend()
    assert plt.gca().get_legend() is not None

