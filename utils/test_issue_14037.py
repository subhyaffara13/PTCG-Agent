
def test_issue_14037():
    assert residue(sin(x**50)/x**51, x, 0) == 1


def test_issue_14037():
    assert (sin(x**50)/x**51).series(x, n=0) == 1/x + O(1, x)

