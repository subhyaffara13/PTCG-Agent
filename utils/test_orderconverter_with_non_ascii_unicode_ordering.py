
def test_orderconverter_with_nonASCII_unicode_ordering():
    # gh-7475
    a = np.arange(5)
    assert_raises(ValueError, a.flatten, order='\xe2')

