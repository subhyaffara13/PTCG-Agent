
def test_cross_figure_patch_legend():
    fig, ax = plt.subplots()
    fig2, ax2 = plt.subplots()

    brs = ax.bar(range(3), range(3))
    fig2.legend(brs, 'foo')

