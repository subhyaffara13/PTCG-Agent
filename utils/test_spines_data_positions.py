
def test_spines_data_positions():
    fig, ax = plt.subplots()
    ax.spines.left.set_position(('data', -1.5))
    ax.spines.top.set_position(('data', 0.5))
    ax.spines.right.set_position(('data', -0.5))
    ax.spines.bottom.set_position('zero')
    ax.set_xlim([-2, 2])
    ax.set_ylim([-2, 2])
    ax.xaxis.set_ticks_position('both')
    ax.yaxis.set_ticks_position('both')

