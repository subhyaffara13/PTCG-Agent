
def test_bar_timedelta():
    """Smoketest that bar can handle width and height in delta units."""
    fig, ax = plt.subplots()
    ax.bar(datetime.datetime(2018, 1, 1), 1.,
           width=datetime.timedelta(hours=3))
    ax.bar(datetime.datetime(2018, 1, 1), 1.,
           xerr=datetime.timedelta(hours=2),
           width=datetime.timedelta(hours=3))
    fig, ax = plt.subplots()
    ax.barh(datetime.datetime(2018, 1, 1), 1,
            height=datetime.timedelta(hours=3))
    ax.barh(datetime.datetime(2018, 1, 1), 1,
            height=datetime.timedelta(hours=3),
            yerr=datetime.timedelta(hours=2))
    fig, ax = plt.subplots()
    ax.barh([datetime.datetime(2018, 1, 1), datetime.datetime(2018, 1, 1)],
            np.array([1, 1.5]),
            height=datetime.timedelta(hours=3))
    ax.barh([datetime.datetime(2018, 1, 1), datetime.datetime(2018, 1, 1)],
            np.array([1, 1.5]),
            height=[datetime.timedelta(hours=t) for t in [1, 2]])
    ax.broken_barh([(datetime.datetime(2018, 1, 1),
                     datetime.timedelta(hours=1))],
                   (10, 20))

