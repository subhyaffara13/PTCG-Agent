
def test_solve_conjugate():
    """Test solve for simple conjugate functions"""
    assert solve(conjugate(x) -3 + I) == [3 + I]

