
def test_issue_14144():
    assert Abs(integrate(1/sqrt(1 - x**3), (x, 0, 1)).n() - 1.402182) < 1e-6
    assert Abs(integrate(sqrt(1 - x**3), (x, 0, 1)).n() - 0.841309) < 1e-6

