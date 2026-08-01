
def test_issue_18689():
    assert floor(floor(floor(x)) + 3) == floor(x) + 3
    assert ceiling(ceiling(ceiling(x)) + 1) == ceiling(x) + 1
    assert ceiling(ceiling(floor(x)) + 3) == floor(x) + 3

