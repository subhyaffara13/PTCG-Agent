
def test_radial_limits_behavior():
    # r=0 is kept as limit if positive data and ticks are used
    # negative ticks or data result in negative limits
    fig = plt.figure()
    ax = fig.add_subplot(projection='polar')
    assert ax.get_ylim() == (0, 1)
    # upper limit is expanded to include the ticks, but lower limit stays at 0
    ax.set_rticks([1, 2, 3, 4])
    assert ax.get_ylim() == (0, 4)
    # upper limit is autoscaled to data, but lower limit limit stays 0
    ax.plot([1, 2], [1, 2])
    assert ax.get_ylim() == (0, 2)
    # negative ticks also expand the negative limit
    ax.set_rticks([-1, 0, 1, 2])
    assert ax.get_ylim() == (-1, 2)
    # negative data also autoscales to negative limits
    ax.plot([1, 2], [-1, -2])
    assert ax.get_ylim() == (-2, 2)

