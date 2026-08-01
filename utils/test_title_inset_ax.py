
def test_title_inset_ax():
    # Title should be above any child axes
    mpl.rcParams['axes.titley'] = None
    fig, ax = plt.subplots()
    ax.set_title('Title')
    fig.draw_without_rendering()
    assert ax.title.get_position()[1] == 1
    ax.inset_axes([0, 1, 1, 0.1])
    fig.draw_without_rendering()
    assert ax.title.get_position()[1] == 1.1

