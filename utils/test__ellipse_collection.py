
def test_EllipseCollection():
    # Test basic functionality
    fig, ax = plt.subplots()
    x = np.arange(4)
    y = np.arange(3)
    X, Y = np.meshgrid(x, y)
    XY = np.vstack((X.ravel(), Y.ravel())).T

    ww = X / x[-1]
    hh = Y / y[-1]
    aa = np.ones_like(ww) * 20  # first axis is 20 degrees CCW from x axis

    ec = mcollections.EllipseCollection(
        ww, hh, aa, units='x', offsets=XY, offset_transform=ax.transData,
        facecolors='none')
    ax.add_collection(ec)

