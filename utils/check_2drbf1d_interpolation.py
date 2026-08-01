
def check_2drbf1d_interpolation(function):
    # Check that the 2-D Rbf function interpolates through the nodes (1D)
    x = linspace(0, 10, 9)
    y0 = sin(x)
    y1 = cos(x)
    y = np.vstack([y0, y1]).T
    rbf = Rbf(x, y, function=function, mode='N-D')
    yi = rbf(x)
    assert_array_almost_equal(y, yi)
    assert_almost_equal(rbf(float(x[0])), y[0])

