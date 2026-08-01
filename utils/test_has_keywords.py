
def test_has_keywords():
    assert has_keywords(lambda: None) is False
    assert has_keywords(lambda x: None) is False
    assert has_keywords(lambda x=1: None)
    assert has_keywords(lambda **kwargs: None)
    assert has_keywords(int)
    assert has_keywords(sorted)
    assert has_keywords(max)
    # map gained `strict=False` keyword in Python 3.14
    assert has_keywords(map) == (sys.version_info[1] >= 14)
    assert has_keywords(bytearray) is None

