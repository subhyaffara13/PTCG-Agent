
def test_colorbar_axes_kw():
    # test fix for #8493: This does only test, that axes-related keywords pass
    # and do not raise an exception.
    plt.figure()
    plt.imshow([[1, 2], [3, 4]])
    plt.colorbar(orientation='horizontal', fraction=0.2, pad=0.2, shrink=0.5,
                 aspect=10, anchor=(0., 0.), panchor=(0., 1.))

