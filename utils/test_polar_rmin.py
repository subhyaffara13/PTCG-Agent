
def test_polar_rmin():
    r = np.arange(0, 3.0, 0.01)
    theta = 2*np.pi*r

    fig = plt.figure()
    ax = fig.add_axes((0.1, 0.1, 0.8, 0.8), polar=True)
    ax.plot(theta, r)
    ax.set_rmax(2.0)
    ax.set_rmin(0.5)

