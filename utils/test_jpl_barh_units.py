
def test_jpl_barh_units():
    import matplotlib.testing.jpl_units as units
    units.register()

    day = units.Duration("ET", 24.0 * 60.0 * 60.0)
    x = [0 * units.km, 1 * units.km, 2 * units.km]
    w = [1 * day, 2 * day, 3 * day]
    b = units.Epoch("ET", dt=datetime(2009, 4, 26))

    fig, ax = plt.subplots()
    ax.barh(x, w, left=b)
    ax.set_xlim([b - 1 * day, b + w[-1] + (1.001) * day])

