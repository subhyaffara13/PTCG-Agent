
def test_tick_space_size_0():
    # allow font size to be zero, which affects ticks when there is
    # no other text in the figure.
    plt.plot([0, 1], [0, 1])
    matplotlib.rcParams.update({'font.size': 0})
    b = io.BytesIO()
    plt.savefig(b, dpi=80, format='raw')

