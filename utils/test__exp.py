
def test_Exp():
    assert str(E) == "E"
    with _exp_is_pow(True):
        assert str(exp(x)) == "E**x"

