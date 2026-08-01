
def test_axes3d_labelpad():
    fig = plt.figure()
    ax = fig.add_axes(Axes3D(fig))
    # labelpad respects rcParams
    assert ax.xaxis.labelpad == mpl.rcParams['axes.labelpad']
    # labelpad can be set in set_label
    ax.set_xlabel('X LABEL', labelpad=10)
    assert ax.xaxis.labelpad == 10
    ax.set_ylabel('Y LABEL')
    ax.set_zlabel('Z LABEL', labelpad=20)
    assert ax.zaxis.labelpad == 20
    assert ax.get_zlabel() == 'Z LABEL'
    # or manually
    ax.yaxis.labelpad = 20
    ax.zaxis.labelpad = -40

    # Tick labels also respect tick.pad (also from rcParams)
    for i, tick in enumerate(ax.yaxis.get_major_ticks()):
        tick.set_pad(tick.get_pad() + 5 - i * 5)

