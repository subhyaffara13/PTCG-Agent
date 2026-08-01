
def test_eventplot_units_list(fig_test, fig_ref):
    # test that list of lists converted properly:
    ts_1 = [datetime.datetime(2021, 1, 1), datetime.datetime(2021, 1, 2),
            datetime.datetime(2021, 1, 3)]
    ts_2 = [datetime.datetime(2021, 1, 15), datetime.datetime(2021, 1, 16)]

    ax = fig_ref.subplots()
    ax.eventplot(ts_1, lineoffsets=0)
    ax.eventplot(ts_2, lineoffsets=1)

    ax = fig_test.subplots()
    ax.eventplot([ts_1, ts_2])

