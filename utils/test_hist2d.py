
def test_hist2d():
    # Remove this line when this test image is regenerated.
    plt.rcParams['pcolormesh.snap'] = False

    np.random.seed(0)
    # make it not symmetric in case we switch x and y axis
    x = np.random.randn(100)*2+5
    y = np.random.randn(100)-2
    fig, ax = plt.subplots()
    ax.hist2d(x, y, bins=10, rasterized=True)

    # Reuse testcase from above for a labeled data test
    data = {"x": x, "y": y}
    fig, ax = plt.subplots()
    ax.hist2d("x", "y", bins=10, data=data, rasterized=True)

