
def test_issue_1561():
    """check fix for issue #1561"""
    bar = m.Issue1561Outer()
    bar.list = [m.Issue1561Inner("bar")]
    assert bar.list
    assert bar.list[0].data == "bar"

