
def test_hashing_sympy_integers():
    # Test for issue 5072
    assert {Integer(3)} == {int(3)}
    assert hash(Integer(4)) == hash(int(4))

