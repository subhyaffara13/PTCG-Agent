
def test_NullFormatter():
    formatter = mticker.NullFormatter()
    assert formatter(1.0) == ''
    assert formatter.format_data(1.0) == ''
    assert formatter.format_data_short(1.0) == ''

