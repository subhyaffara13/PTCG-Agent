
def test_clabel_raises_on_filled_contours():
    X, Y = np.meshgrid(np.arange(10), np.arange(10))
    _, ax = plt.subplots()
    cs = ax.contourf(X, Y, X + Y)
    # will be an exception once the deprecation expires
    with pytest.warns(mpl.MatplotlibDeprecationWarning):
        ax.clabel(cs)

