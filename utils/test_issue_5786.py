
def test_issue_5786():
    assert expand(factor(expand(
        (x - I*y)*(z - I*t)), extension=[I])) == -I*t*x - t*y + x*z - I*y*z

