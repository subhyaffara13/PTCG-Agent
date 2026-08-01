
def test_get_packed_offsets_expand(widths, total, sep, expected):
    result = _get_packed_offsets(widths, total, sep, mode='expand')
    assert result[0] == expected[0]
    assert_allclose(result[1], expected[1])

