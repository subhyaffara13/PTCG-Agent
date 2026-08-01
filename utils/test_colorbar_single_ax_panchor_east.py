
def test_colorbar_single_ax_panchor_east(constrained):
    fig = plt.figure(constrained_layout=constrained)
    ax = fig.add_subplot(111, anchor='N')
    plt.imshow([[0, 1]])
    plt.colorbar(panchor='E')
    assert ax.get_anchor() == 'E'

