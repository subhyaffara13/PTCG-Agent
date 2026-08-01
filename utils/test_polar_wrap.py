
def test_polar_wrap(fig_test, fig_ref):
    ax = fig_test.add_subplot(projection="polar")
    ax.plot(np.deg2rad([179, -179]), [0.2, 0.1])
    ax.plot(np.deg2rad([2, -2]), [0.2, 0.1])
    ax = fig_ref.add_subplot(projection="polar")
    ax.plot(np.deg2rad([179, 181]), [0.2, 0.1])
    ax.plot(np.deg2rad([2, 358]), [0.2, 0.1])

