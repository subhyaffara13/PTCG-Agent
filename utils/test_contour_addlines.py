
def test_contour_addlines():
    # Remove this line when this test image is regenerated.
    plt.rcParams['pcolormesh.snap'] = False

    fig, ax = plt.subplots()
    np.random.seed(19680812)
    X = np.random.rand(10, 10)*10000
    pcm = ax.pcolormesh(X)
    # add 1000 to make colors visible...
    cont = ax.contour(X+1000)
    cb = fig.colorbar(pcm)
    cb.add_lines(cont)
    assert_array_almost_equal(cb.ax.get_ylim(), [114.3091, 9972.30735], 3)

