
def test_test_unicode_encoding():
    unicode_whitelist = ['foo']
    unicode_strict_whitelist = ['bar']

    fname = 'abc'
    test_file = ['α']
    raises(AssertionError, lambda: _test_this_file_encoding(
        fname, test_file, unicode_whitelist, unicode_strict_whitelist))

    fname = 'abc'
    test_file = ['abc']
    _test_this_file_encoding(
        fname, test_file, unicode_whitelist, unicode_strict_whitelist)

    fname = 'foo'
    test_file = ['abc']
    raises(AssertionError, lambda: _test_this_file_encoding(
        fname, test_file, unicode_whitelist, unicode_strict_whitelist))

    fname = 'bar'
    test_file = ['abc']
    _test_this_file_encoding(
        fname, test_file, unicode_whitelist, unicode_strict_whitelist)

