
def test_contourf_symmetric_locator():
    # github issue 7271
    z = np.arange(12).reshape((3, 4))
    locator = plt.MaxNLocator(nbins=4, symmetric=True)
    cs = plt.contourf(z, locator=locator)
    assert_array_almost_equal(cs.levels, np.linspace(-12, 12, 5))

