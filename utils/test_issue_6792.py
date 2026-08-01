
def test_issue_6792():
    assert solve(x*(x - 1)**2*(x + 1)*(x**6 - x + 1)) == [
        -1, 0, 1, CRootOf(x**6 - x + 1, 0), CRootOf(x**6 - x + 1, 1),
         CRootOf(x**6 - x + 1, 2), CRootOf(x**6 - x + 1, 3),
         CRootOf(x**6 - x + 1, 4), CRootOf(x**6 - x + 1, 5)]

