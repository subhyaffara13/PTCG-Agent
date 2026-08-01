
def test_backend_plan(func, mock):
    x = np.arange(20).reshape((10, 2))

    with pytest.raises(NotImplementedError, match='precomputed plan'):
        func(x, plan='foo')

    with set_backend(mock_backend, only=True):
        mock.number_calls.c = 0
        y = func(x, plan='foo')
        assert_equal(y, mock.return_value)
        assert_equal(mock.number_calls.c, 1)
        assert_equal(mock.last_args.l[1]['plan'], 'foo')

