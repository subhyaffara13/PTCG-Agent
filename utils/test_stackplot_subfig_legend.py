
def test_stackplot_subfig_legend():
    # Smoke test for https://github.com/matplotlib/matplotlib/issues/30158

    fig = plt.figure()
    subfigs = fig.subfigures(nrows=1, ncols=2)

    for _fig in subfigs:
        ax = _fig.subplots(nrows=1, ncols=1)
        ax.stackplot([3, 4], [[1, 2]], labels=['a'])

    fig.legend()
    fig.draw_without_rendering()

