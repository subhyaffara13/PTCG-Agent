
def test_pad_dict_pad_width(input_shape, pad_width, expected_shape):
    a = np.zeros(input_shape)
    result = np.pad(a, pad_width)
    assert result.shape == expected_shape

