
def test_title_no_move_off_page():
    # If an Axes is off the figure (ie. if it is cropped during a save)
    # make sure that the automatic title repositioning does not get done.
    mpl.rcParams['axes.titley'] = None
    fig = plt.figure()
    ax = fig.add_axes((0.1, -0.5, 0.8, 0.2))
    ax.tick_params(axis="x",
                   bottom=True, top=True, labelbottom=True, labeltop=True)
    tt = ax.set_title('Boo')
    fig.canvas.draw()
    assert tt.get_position()[1] == 1.0

