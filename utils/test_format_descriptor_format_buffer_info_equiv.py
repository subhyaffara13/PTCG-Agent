
def test_format_descriptor_format_buffer_info_equiv(cpp_name, np_dtype):
    if np_dtype is None:
        pytest.skip(
            f"cpp_name=`{cpp_name}`: `long double` and `double` have same size."
        )
    if isinstance(np_dtype, str):
        pytest.skip(f"np.{np_dtype} does not exist.")
    np_array = np.array([], dtype=np_dtype)
    for other_cpp_name, expected_format in CPP_NAME_FORMAT_TABLE:
        format, np_array_is_matching = m.format_descriptor_format_buffer_info_equiv(
            other_cpp_name, np_array
        )
        assert format == expected_format
        if other_cpp_name == cpp_name:
            assert np_array_is_matching
        else:
            assert not np_array_is_matching

