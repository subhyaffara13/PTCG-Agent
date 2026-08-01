
def test_invalid_integers():
    with pytest.raises(TypeError,
            match="integer argument expected, got float"):
        func(1.)
    with pytest.raises(OverflowError):
        func(2**100)

