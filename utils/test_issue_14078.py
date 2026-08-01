
def test_issue_14078():
    assert integrate((cos(3*x)-cos(x))/x, (x, 0, oo)) == -log(3)

