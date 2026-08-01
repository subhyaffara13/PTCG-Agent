
def test_invisible_ticks_axis():
    fig = plt.figure()
    ax = fig.add_subplot(projection='3d')
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_zticks([])
    for axis in [ax.xaxis, ax.yaxis, ax.zaxis]:
        axis.line.set_visible(False)

