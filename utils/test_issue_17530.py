
def test_issue_17530():
    r = {x: oo, y: oo}
    assert Or(x + y > 0, x - y < 0).subs(r)
    assert not And(x + y < 0, x - y < 0).subs(r)
    raises(TypeError, lambda: Or(x + y < 0, x - y < 0).subs(r))
    raises(TypeError, lambda: And(x + y > 0, x - y < 0).subs(r))
    raises(TypeError, lambda: And(x + y > 0, x - y < 0).subs(r))

