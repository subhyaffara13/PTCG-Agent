
def test_title_xticks_top_both():
    # Test that title moves if xticks on top of axes.
    mpl.rcParams['axes.titley'] = None
    fig, ax = plt.subplots()
    ax.tick_params(axis="x",
                   bottom=True, top=True, labelbottom=True, labeltop=True)
    ax.set_title('xlabel top')
    fig.canvas.draw()
    assert ax.title.get_position()[1] > 1.04

