
def test_get_output_complex():
    shape = (2, 3)

    input_ = np.zeros(shape)

    # None, promote input type to complex
    result = _get_output(None, input_, complex_output=True)
    assert result.shape == shape
    assert result.dtype == np.dtype('complex128')

    # Explicit type, promote type to complex
    with pytest.warns(UserWarning, match='promoting specified output dtype to complex'):
        result = _get_output(float, input_, complex_output=True)
    assert result.shape == shape
    assert result.dtype == np.dtype('complex128')

    # String specifier, simply verify complex output
    result = _get_output('complex64', input_, complex_output=True)
    assert result.shape == shape
    assert result.dtype == np.dtype('complex64')

