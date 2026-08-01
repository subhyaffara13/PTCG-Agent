
def test_issue_15852():
    assert summation(x**y*y, (y, -oo, oo)).doit() == Sum(x**y*y, (y, -oo, oo))

