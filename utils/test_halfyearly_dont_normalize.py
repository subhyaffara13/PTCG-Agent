
def test_halfyearly_dont_normalize(klass):
    date = datetime(2012, 3, 31, 5, 30)
    result = date + klass()
    assert result.time() == date.time()


def test_halfyearly_dont_normalize(klass):
    date = datetime(2012, 3, 31, 5, 30)
    result = date + klass()
    assert result.time() == date.time()

