
def test_axis_positions():
    positions = ['upper', 'lower', 'both', 'none']
    fig, axs = plt.subplots(2, 2, subplot_kw={'projection': '3d'})
    for ax, pos in zip(axs.flatten(), positions):
        for axis in ax.xaxis, ax.yaxis, ax.zaxis:
            axis.set_label_position(pos)
            axis.set_ticks_position(pos)
        title = f'{pos}'
        ax.set(xlabel='x', ylabel='y', zlabel='z', title=title)

