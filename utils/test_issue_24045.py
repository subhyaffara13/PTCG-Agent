
def test_issue_24045():
    assert powsimp(exp(a)/((c*a - c*b)*(Float(1.0)*c*a - Float(1.0)*c*b)))  # doesn't raise

