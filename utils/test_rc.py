
def test_rc():
    # using subplot triggers some offsetbox functionality untested elsewhere
    mpl.rcParams['legend.scatterpoints'] = 3
    plt.figure()
    ax = plt.subplot(121)
    ax.scatter(np.arange(10), np.arange(10, 0, -1), label='three')
    ax.legend(loc="center left", bbox_to_anchor=[1.0, 0.5],
              title="My legend")

    mpl.rcParams['legend.scatterpoints'] = 1
    plt.figure()
    ax = plt.subplot(121)
    ax.scatter(np.arange(10), np.arange(10, 0, -1), label='one')
    ax.legend(loc="center left", bbox_to_anchor=[1.0, 0.5],
              title="My legend")

