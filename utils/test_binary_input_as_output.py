
def test_binary_input_as_output(func, iterations, brute_force, xp):
    rstate = np.random.RandomState(123)
    data = rstate.randint(low=0, high=2, size=100).astype(bool)
    data = xp.asarray(data)

    # input data is not modified
    data_orig = data.copy()
    expected = func(data, brute_force=brute_force, iterations=iterations)
    xp_assert_equal(data, data_orig)

    # data should now contain the expected result
    func(data, brute_force=brute_force, iterations=iterations, output=data)
    xp_assert_equal(data, expected)

