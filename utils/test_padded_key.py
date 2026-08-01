
def test_padded_key():
    assert padded_key('b', 'ab') == 'ba'
    raises(ValueError, lambda: padded_key('ab', 'ace'))
    raises(ValueError, lambda: padded_key('ab', 'abba'))

