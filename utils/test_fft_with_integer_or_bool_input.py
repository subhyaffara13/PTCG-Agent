
def test_fft_with_integer_or_bool_input(data, fft):
    # Regression test for gh-25819
    result = fft(data)
    float_data = data.astype(np.result_type(data, 1.))
    expected = fft(float_data)
    assert_array_equal(result, expected)

