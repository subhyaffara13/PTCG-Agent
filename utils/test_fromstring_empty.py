
def test_fromstring_empty():
    with assert_raises(ValueError):
        np.fromstring("xxxxx", sep="x")

