
def test_center_accent():
    assert center_accent('a', '\N{COMBINING TILDE}') == 'ã'
    assert center_accent('aa', '\N{COMBINING TILDE}') == 'aã'
    assert center_accent('aaa', '\N{COMBINING TILDE}') == 'aãa'
    assert center_accent('aaaa', '\N{COMBINING TILDE}') == 'aaãa'
    assert center_accent('aaaaa', '\N{COMBINING TILDE}') == 'aaãaa'
    assert center_accent('abcdefg', '\N{COMBINING FOUR DOTS ABOVE}') == 'abcd⃜efg'

