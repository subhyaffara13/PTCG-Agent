
def test_fromstring_bogus():
    with assert_raises(ValueError):
        np.fromstring("1. 2. 3. flop 4.", dtype=float, sep=" ")

