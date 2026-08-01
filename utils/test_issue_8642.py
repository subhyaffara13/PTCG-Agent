
def test_issue_8642():
    x = Symbol('x', real=True, integer=False)
    assert (x*2).is_integer is None, (x*2).is_integer

