
def test_backend_call(func, np_func, mock):
    x = np.arange(20).reshape((10,2))
    answer = np_func(x.astype(np.float64))
    assert_allclose(func(x), answer, atol=1e-10)

    with set_backend(mock_backend, only=True):
        mock.number_calls.c = 0
        y = func(x)
        assert_equal(y, mock.return_value)
        assert_equal(mock.number_calls.c, 1)

    assert_allclose(func(x), answer, atol=1e-10)

