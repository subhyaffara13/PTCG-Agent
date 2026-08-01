
def test_get_dtype_fails(input_param, expected_error_message):
    # python objects
    # 2020-02-02 npdev changed error message
    expected_error_message += f"|Cannot interpret '{input_param}' as a data type"
    with pytest.raises(TypeError, match=expected_error_message):
        com._get_dtype(input_param)

