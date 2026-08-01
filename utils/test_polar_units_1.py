
def test_polar_units_1(fig_test, fig_ref):
    import matplotlib.testing.jpl_units as units
    units.register()
    xs = [30.0, 45.0, 60.0, 90.0]
    ys = [1.0, 2.0, 3.0, 4.0]

    plt.figure(fig_test)
    plt.polar([x * units.deg for x in xs], ys)

    ax = fig_ref.add_subplot(projection="polar")
    ax.plot(np.deg2rad(xs), ys)
    ax.set(xlabel="deg")

