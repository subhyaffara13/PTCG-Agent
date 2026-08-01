
def test_issue_8439():
    assert sympify(float('inf')) == oo
    assert x + float('inf') == x + oo
    assert S(float('inf')) == oo

