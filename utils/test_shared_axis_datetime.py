
def test_shared_axis_datetime():
    # datetime uses dates.DateConverter
    y1 = [datetime(2020, i, 1, tzinfo=timezone.utc) for i in range(1, 13)]
    y2 = [datetime(2021, i, 1, tzinfo=timezone.utc) for i in range(1, 13)]
    fig, (ax1, ax2) = plt.subplots(1, 2, sharey=True)
    ax1.plot(y1)
    ax2.plot(y2)
    ax1.yaxis.set_units(timezone(timedelta(hours=5)))
    assert ax2.yaxis.units == timezone(timedelta(hours=5))

