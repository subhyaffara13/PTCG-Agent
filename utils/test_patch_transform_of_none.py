
def test_patch_transform_of_none():
    # tests the behaviour of patches added to an Axes with various transform
    # specifications

    ax = plt.axes()
    ax.set_xlim(1, 3)
    ax.set_ylim(1, 3)

    # Draw an ellipse over data coord (2, 2) by specifying device coords.
    xy_data = (2, 2)
    xy_pix = ax.transData.transform(xy_data)

    # Not providing a transform of None puts the ellipse in data coordinates .
    e = mpatches.Ellipse(xy_data, width=1, height=1, fc='yellow', alpha=0.5)
    ax.add_patch(e)
    assert e._transform == ax.transData

    # Providing a transform of None puts the ellipse in device coordinates.
    e = mpatches.Ellipse(xy_pix, width=120, height=120, fc='coral',
                         transform=None, alpha=0.5)
    assert e.is_transform_set()
    ax.add_patch(e)
    assert isinstance(e._transform, mtransforms.IdentityTransform)

    # Providing an IdentityTransform puts the ellipse in device coordinates.
    e = mpatches.Ellipse(xy_pix, width=100, height=100,
                         transform=mtransforms.IdentityTransform(), alpha=0.5)
    ax.add_patch(e)
    assert isinstance(e._transform, mtransforms.IdentityTransform)

    # Not providing a transform, and then subsequently "get_transform" should
    # not mean that "is_transform_set".
    e = mpatches.Ellipse(xy_pix, width=120, height=120, fc='coral',
                         alpha=0.5)
    intermediate_transform = e.get_transform()
    assert not e.is_transform_set()
    ax.add_patch(e)
    assert e.get_transform() != intermediate_transform
    assert e.is_transform_set()
    assert e._transform == ax.transData

