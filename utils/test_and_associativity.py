
def test_and_associativity():
    """Test for associativity of And"""

    assert (A & B) & C == A & (B & C)

