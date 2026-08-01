
def test_imshow():
    # use former defaults to match existing baseline image
    matplotlib.rcParams['image.interpolation'] = 'nearest'
    # Create an NxN image
    N = 100
    (x, y) = np.indices((N, N))
    x -= N//2
    y -= N//2
    r = np.sqrt(x**2+y**2-x*y)

    # Create a contour plot at N/4 and extract both the clip path and transform
    fig, ax = plt.subplots()
    ax.imshow(r)

    # Reuse testcase from above for a labeled data test
    data = {"r": r}
    fig, ax = plt.subplots()
    ax.imshow("r", data=data)

