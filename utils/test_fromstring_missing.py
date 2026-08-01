
def test_fromstring_missing():
    with assert_raises(ValueError):
        np.fromstring("1xx3x4x5x6", sep="x")

