
def test_bool_symbol():
    """Test that mixing symbols with boolean values
    works as expected"""

    assert And(A, True) == A
    assert And(A, True, True) == A
    assert And(A, False) is false
    assert And(A, True, False) is false
    assert Or(A, True) is true
    assert Or(A, False) == A

