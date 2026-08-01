
def test_Modulus_preprocess():
    assert Modulus.preprocess(23) == 23
    assert Modulus.preprocess(Integer(23)) == 23

    raises(OptionError, lambda: Modulus.preprocess(0))
    raises(OptionError, lambda: Modulus.preprocess(x))

