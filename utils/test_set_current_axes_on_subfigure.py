
def test_set_current_axes_on_subfigure():
    fig = plt.figure()
    subfigs = fig.subfigures(2)

    ax = subfigs[0].subplots(1, squeeze=True)
    subfigs[1].subplots(1, squeeze=True)

    assert plt.gca() != ax
    plt.sca(ax)
    assert plt.gca() == ax

