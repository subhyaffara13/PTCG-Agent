
def test_default_construction():
    # Check that the Rbf class can be constructed with the default
    # multiquadric basis function. Regression test for ticket #1228.
    x = linspace(0,10,9)
    y = sin(x)
    rbf = Rbf(x, y)
    yi = rbf(x)
    assert_array_almost_equal(y, yi)

