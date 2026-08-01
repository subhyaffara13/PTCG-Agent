
def test_as_mpl_axes_api():
    # tests the _as_mpl_axes api
    class Polar:
        def __init__(self):
            self.theta_offset = 0

        def _as_mpl_axes(self):
            # implement the matplotlib axes interface
            return PolarAxes, {'theta_offset': self.theta_offset}

    prj = Polar()
    prj2 = Polar()
    prj2.theta_offset = np.pi

    # testing axes creation with plt.axes
    ax = plt.axes((0, 0, 1, 1), projection=prj)
    assert type(ax) is PolarAxes
    plt.close()

    # testing axes creation with subplot
    ax = plt.subplot(121, projection=prj)
    assert type(ax) is PolarAxes
    plt.close()

