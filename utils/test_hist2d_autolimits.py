
def test_hist2d_autolimits():
    x, y = np.random.random((2, 100))
    ax = plt.figure().add_subplot()
    ax.hist2d(x, y)
    assert ax.get_xlim() == (x.min(), x.max())
    assert ax.get_ylim() == (y.min(), y.max())
    assert ax.get_autoscale_on()  # Autolimits have not been disabled.

