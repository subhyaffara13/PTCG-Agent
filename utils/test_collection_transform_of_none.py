
def test_collection_transform_of_none():
    # tests the behaviour of collections added to an Axes with various
    # transform specifications

    ax = plt.axes()
    ax.set_xlim(1, 3)
    ax.set_ylim(1, 3)

    # draw an ellipse over data coord (2, 2) by specifying device coords
    xy_data = (2, 2)
    xy_pix = ax.transData.transform(xy_data)

    # not providing a transform of None puts the ellipse in data coordinates
    e = mpatches.Ellipse(xy_data, width=1, height=1)
    c = mcollections.PatchCollection([e], facecolor='yellow', alpha=0.5)
    ax.add_collection(c)
    # the collection should be in data coordinates
    assert c.get_offset_transform() + c.get_transform() == ax.transData

    # providing a transform of None puts the ellipse in device coordinates
    e = mpatches.Ellipse(xy_pix, width=120, height=120)
    c = mcollections.PatchCollection([e], facecolor='coral',
                                     alpha=0.5)
    c.set_transform(None)
    ax.add_collection(c)
    assert isinstance(c.get_transform(), mtransforms.IdentityTransform)

    # providing an IdentityTransform puts the ellipse in device coordinates
    e = mpatches.Ellipse(xy_pix, width=100, height=100)
    c = mcollections.PatchCollection([e],
                                     transform=mtransforms.IdentityTransform(),
                                     alpha=0.5)
    ax.add_collection(c)
    assert isinstance(c.get_offset_transform(), mtransforms.IdentityTransform)

