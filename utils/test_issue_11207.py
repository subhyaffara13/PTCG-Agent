
def test_issue_11207():
    assert floor(floor(x)) == floor(x)
    assert floor(ceiling(x)) == ceiling(x)
    assert ceiling(floor(x)) == floor(x)
    assert ceiling(ceiling(x)) == ceiling(x)

