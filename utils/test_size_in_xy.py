
def test_size_in_xy():
    fig, ax = plt.subplots()

    widths, heights, angles = (10, 10), 10, 0
    widths = 10, 10
    coords = [(10, 10), (15, 15)]
    e = mcollections.EllipseCollection(
        widths, heights, angles, units='xy',
        offsets=coords, offset_transform=ax.transData)

    ax.add_collection(e)

    ax.set_xlim(0, 30)
    ax.set_ylim(0, 30)

