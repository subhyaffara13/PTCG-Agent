
def test_mollweide_grid():
    # test that both horizontal and vertical gridlines appear on the Mollweide
    # projection
    fig = plt.figure()
    ax = fig.add_subplot(projection='mollweide')
    ax.grid()

