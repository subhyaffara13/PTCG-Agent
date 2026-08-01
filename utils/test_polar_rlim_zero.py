
def test_polar_rlim_zero():
    ax = plt.figure().add_subplot(projection='polar')
    ax.plot(np.arange(10), np.arange(10) + .01)
    assert ax.get_ylim()[0] == 0

