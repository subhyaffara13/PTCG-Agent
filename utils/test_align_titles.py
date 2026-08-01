
def test_align_titles():
    for layout in ['tight', 'constrained']:
        fig, axs = plt.subplots(1, 2, layout=layout, width_ratios=[2, 1])

        ax = axs[0]
        ax.plot(np.arange(0, 1e6, 1000))
        ax.set_title('Title0 left', loc='left')
        ax.set_title('Title0 center', loc='center')
        ax.set_title('Title0 right', loc='right')

        ax = axs[1]
        ax.plot(np.arange(0, 1e4, 100))
        ax.set_title('Title1')
        ax.set_xlabel('Xlabel0')
        ax.xaxis.set_label_position("top")
        ax.xaxis.tick_top()
        for tick in ax.get_xticklabels():
            tick.set_rotation(90)

        fig.align_titles()

