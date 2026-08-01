
def test_get_output_error_cases():
    input_ = np.zeros((2, 3), 'float32')

    # Two separate paths can raise the same error
    with pytest.raises(RuntimeError, match='output must have complex dtype'):
        _get_output('float32', input_, complex_output=True)
    with pytest.raises(RuntimeError, match='output must have complex dtype'):
        _get_output(np.zeros((2, 3)), input_, complex_output=True)

    with pytest.raises(RuntimeError, match='output must have numeric dtype'):
        _get_output('void', input_)

    with pytest.raises(RuntimeError, match='shape not correct'):
        _get_output(np.zeros((3, 2)), input_)

