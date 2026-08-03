import re

def test_datetime_indexing():
    index = date_range("1/1/2000", "1/7/2000")
    index = index.repeat(3)

    s = Series(len(index), index=index)
    stamp = Timestamp("1/8/2000")

    with pytest.raises(KeyError, match=re.escape(repr(stamp))):
        s[stamp]
    s[stamp] = 0
    assert s[stamp] == 0

    # not monotonic
    s = Series(len(index), index=index)
    s = s[::-1]

    with pytest.raises(KeyError, match=re.escape(repr(stamp))):
        s[stamp]
    s[stamp] = 0
    assert s[stamp] == 0

