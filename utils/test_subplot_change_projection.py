
def test_subplot_change_projection():
    created_axes = set()
    ax = plt.subplot()
    created_axes.add(ax)
    projections = ('aitoff', 'hammer', 'lambert', 'mollweide',
                   'polar', 'rectilinear', '3d')
    for proj in projections:
        ax.remove()
        ax = plt.subplot(projection=proj)
        assert ax is plt.subplot()
        assert ax.name == proj
        created_axes.add(ax)
    # Check that each call created a new Axes.
    assert len(created_axes) == 1 + len(projections)

