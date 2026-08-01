
def test_quarterly_dont_normalize():
    date = datetime(2012, 3, 31, 5, 30)

    offsets = (BQuarterEnd, BQuarterBegin)

    for klass in offsets:
        result = date + klass()
        assert result.time() == date.time()


def test_quarterly_dont_normalize(klass):
    date = datetime(2012, 3, 31, 5, 30)
    result = date + klass()
    assert result.time() == date.time()

