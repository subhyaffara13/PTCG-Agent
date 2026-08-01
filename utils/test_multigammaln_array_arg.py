
def test_multigammaln_array_arg():
    # Check that the array returned by multigammaln has the correct
    # shape and contains the correct values.  The cases have arrays
    # with several different shapes.
    # The cases include a regression test for ticket #1849
    # (a = np.array([2.0]), an array with a single element).
    np.random.seed(1234)

    cases = [
        # a, d
        (np.abs(np.random.randn(3, 2)) + 5, 5),
        (np.abs(np.random.randn(1, 2)) + 5, 5),
        (np.arange(10.0, 18.0).reshape(2, 2, 2), 3),
        (np.array([2.0]), 3),
        (np.float64(2.0), 3),
    ]

    for a, d in cases:
        _check_multigammaln_array_result(a, d)

