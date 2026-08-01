
def test_axis_extent_arg():
    fig, ax = plt.subplots()
    xmin = 5
    xmax = 10
    ymin = 15
    ymax = 20
    extent = ax.axis([xmin, xmax, ymin, ymax])

    # test that the docstring is correct
    assert tuple(extent) == (xmin, xmax, ymin, ymax)

    # test that limits were set per the docstring
    assert (xmin, xmax) == ax.get_xlim()
    assert (ymin, ymax) == ax.get_ylim()

