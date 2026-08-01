
def test_negative_real():
    def feq(a, b):
        return abs(a - b) < 1E-10

    assert feq(S.One / Float(-0.5), -Integer(2))

