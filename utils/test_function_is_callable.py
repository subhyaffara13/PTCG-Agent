
def test_function_is_callable():
    # Check that the Rbf class can be constructed with function=callable.
    x = linspace(0,10,9)
    y = sin(x)
    def linfunc(x):
        return x
    rbf = Rbf(x, y, function=linfunc)
    yi = rbf(x)
    assert_array_almost_equal(y, yi)

