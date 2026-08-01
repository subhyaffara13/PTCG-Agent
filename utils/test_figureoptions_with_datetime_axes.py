
def test_figureoptions_with_datetime_axes():
    fig, ax = plt.subplots()
    xydata = [
        datetime(year=2021, month=1, day=1),
        datetime(year=2021, month=2, day=1)
    ]
    ax.plot(xydata, xydata)
    with mock.patch("matplotlib.backends.qt_compat._exec", lambda obj: None):
        fig.canvas.manager.toolbar.edit_parameters()

