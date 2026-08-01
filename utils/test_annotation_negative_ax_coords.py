
def test_annotation_negative_ax_coords():
    fig, ax = plt.subplots()

    ax.annotate('+ pts',
                xytext=[30, 20], textcoords='axes points',
                xy=[30, 20], xycoords='axes points', fontsize=32)
    ax.annotate('- pts',
                xytext=[30, -20], textcoords='axes points',
                xy=[30, -20], xycoords='axes points', fontsize=32,
                va='top')
    ax.annotate('+ frac',
                xytext=[0.75, 0.05], textcoords='axes fraction',
                xy=[0.75, 0.05], xycoords='axes fraction', fontsize=32)
    ax.annotate('- frac',
                xytext=[0.75, -0.05], textcoords='axes fraction',
                xy=[0.75, -0.05], xycoords='axes fraction', fontsize=32,
                va='top')

    ax.annotate('+ pixels',
                xytext=[160, 25], textcoords='axes pixels',
                xy=[160, 25], xycoords='axes pixels', fontsize=32)
    ax.annotate('- pixels',
                xytext=[160, -25], textcoords='axes pixels',
                xy=[160, -25], xycoords='axes pixels', fontsize=32,
                va='top')

