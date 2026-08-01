
def test_hist2d_transpose():
    # Remove this line when this test image is regenerated.
    plt.rcParams['pcolormesh.snap'] = False

    np.random.seed(0)
    # make sure the output from np.histogram is transposed before
    # passing to pcolorfast
    x = np.array([5]*100)
    y = np.random.randn(100)-2
    fig, ax = plt.subplots()
    ax.hist2d(x, y, bins=10, rasterized=True)

