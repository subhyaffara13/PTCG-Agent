
def test_pcolor_regression(pd):
    from pandas.plotting import (
        register_matplotlib_converters,
        deregister_matplotlib_converters,
    )

    fig = plt.figure()
    ax = fig.add_subplot(111)

    times = [datetime.datetime(2021, 1, 1)]
    while len(times) < 7:
        times.append(times[-1] + datetime.timedelta(seconds=120))

    y_vals = np.arange(5)

    time_axis, y_axis = np.meshgrid(times, y_vals)
    shape = (len(y_vals) - 1, len(times) - 1)
    z_data = np.arange(shape[0] * shape[1]).reshape(shape)

    try:
        register_matplotlib_converters()

        im = ax.pcolormesh(time_axis, y_axis, z_data)
        # make sure this does not raise!
        fig.canvas.draw()
    finally:
        deregister_matplotlib_converters()

