
def test_stairs_datetime():
    f, ax = plt.subplots(constrained_layout=True)
    ax.stairs(np.arange(36),
              np.arange(np.datetime64('2001-12-27'),
                        np.datetime64('2002-02-02')))
    plt.xticks(rotation=30)

