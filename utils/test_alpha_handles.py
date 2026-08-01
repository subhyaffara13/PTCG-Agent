
def test_alpha_handles():
    x, n, hh = plt.hist([1, 2, 3], alpha=0.25, label='data', color='red')
    legend = plt.legend()
    for lh in legend.legend_handles:
        lh.set_alpha(1.0)
    assert lh.get_facecolor()[:-1] == hh[1].get_facecolor()[:-1]
    assert lh.get_edgecolor()[:-1] == hh[1].get_edgecolor()[:-1]

