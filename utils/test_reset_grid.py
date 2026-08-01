
def test_reset_grid():
    fig, ax = plt.subplots()
    ax.tick_params(reset=True, which='major', labelsize=10)
    assert not ax.xaxis.majorTicks[0].gridline.get_visible()
    ax.grid(color='red')  # enables grid
    assert ax.xaxis.majorTicks[0].gridline.get_visible()

    with plt.rc_context({'axes.grid': True}):
        ax.clear()
        ax.tick_params(reset=True, which='major', labelsize=10)
        assert ax.xaxis.majorTicks[0].gridline.get_visible()

