
def test_maple_not_supported():
    with raises(NotImplementedError):
        maple_code(S.ComplexInfinity)

