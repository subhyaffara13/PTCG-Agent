
def check_rbf1d_interpolation(function):
    # Check that the Rbf function interpolates through the nodes (1D)
    x = linspace(0,10,9)
    y = sin(x)
    rbf = Rbf(x, y, function=function)
    yi = rbf(x)
    assert_array_almost_equal(y, yi)
    assert_almost_equal(rbf(float(x[0])), y[0], check_0d=False)

