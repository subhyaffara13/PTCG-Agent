
def test_set_offset_string(formatter):
    assert formatter.get_offset() == ''
    formatter.set_offset_string('mpl')
    assert formatter.get_offset() == 'mpl'

