
def test_solveset_conjugate():
    """Test solveset for simple conjugate functions"""
    assert solveset(conjugate(x) -3 + I) == FiniteSet(3 + I)

