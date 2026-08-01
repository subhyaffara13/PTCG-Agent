
def test_get_unicode_index_exception():
    with pytest.raises(ValueError):
        _mathtext.get_unicode_index(r'\foo')

