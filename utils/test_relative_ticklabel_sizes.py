
def test_relative_ticklabel_sizes(size):
    mpl.rcParams['xtick.labelsize'] = size
    mpl.rcParams['ytick.labelsize'] = size
    fig, ax = plt.subplots()
    fig.canvas.draw()

    for name, axis in zip(['x', 'y'], [ax.xaxis, ax.yaxis]):
        for tick in axis.get_major_ticks():
            assert tick.label1.get_size() == axis._get_tick_label_size(name)

