
def test_chop_value():
    for i in range(-27, 28):
        assert (Pow(10, i)*2).n(chop=10**i) and not (Pow(10, i)).n(chop=10**i)

