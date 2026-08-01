
def test_anchored_direction_arrows():
    fig, ax = plt.subplots()
    ax.imshow(np.zeros((10, 10)), interpolation='nearest')

    simple_arrow = AnchoredDirectionArrows(ax.transAxes, 'X', 'Y')
    ax.add_artist(simple_arrow)

