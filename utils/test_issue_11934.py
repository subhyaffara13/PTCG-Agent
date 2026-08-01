
def test_issue_11934():
    density = {0: .5, 1: .5}
    X = FiniteRV('X', density)
    assert E(X) == 0.5
    assert P( X>= 2) == 0

