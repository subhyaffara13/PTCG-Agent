
def test_two_arg_function_is_callable():
    # Check that the Rbf class can be constructed with a two argument
    # function=callable.
    def _func(self, r):
        return self.epsilon + r

    x = linspace(0,10,9)
    y = sin(x)
    rbf = Rbf(x, y, function=_func)
    yi = rbf(x)
    assert_array_almost_equal(y, yi)

