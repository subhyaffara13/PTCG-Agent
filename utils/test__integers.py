
def test_Integers():
    assert aesara_code_(sy.Integer(3)) == 3


def test_Integers():
    sT(S.Integers, "Integers")


def test_Integers():
    assert theano_code_(sy.Integer(3)) == 3

