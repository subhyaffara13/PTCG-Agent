
def test_issue_4498():
    assert cse(w/(x - y) + z/(y - x), optimizations='basic') == \
        ([], [(w - z)/(x - y)])

