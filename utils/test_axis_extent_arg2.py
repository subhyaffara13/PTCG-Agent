
def test_axis_extent_arg2():
    # Same as test_axis_extent_arg, but with keyword arguments
    fig, ax = plt.subplots()
    xmin = 5
    xmax = 10
    ymin = 15
    ymax = 20
    extent = ax.axis(xmin=xmin, xmax=xmax, ymin=ymin, ymax=ymax)

    # test that the docstring is correct
    assert tuple(extent) == (xmin, xmax, ymin, ymax)

    # test that limits were set per the docstring
    assert (xmin, xmax) == ax.get_xlim()
    assert (ymin, ymax) == ax.get_ylim()

