
def test_subplot_projection_reuse():
    # create an Axes
    ax1 = plt.subplot(111)
    # check that it is current
    assert ax1 is plt.gca()
    # make sure we get it back if we ask again
    assert ax1 is plt.subplot(111)
    # remove it
    ax1.remove()
    # create a polar plot
    ax2 = plt.subplot(111, projection='polar')
    assert ax2 is plt.gca()
    # this should have deleted the first axes
    assert ax1 not in plt.gcf().axes
    # assert we get it back if no extra parameters passed
    assert ax2 is plt.subplot(111)
    ax2.remove()
    # now check explicitly setting the projection to rectilinear
    # makes a new axes
    ax3 = plt.subplot(111, projection='rectilinear')
    assert ax3 is plt.gca()
    assert ax3 is not ax2
    assert ax2 not in plt.gcf().axes

