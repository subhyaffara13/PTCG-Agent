
def test_issue_16759():
    d = sympify({.5: 1})
    assert S.Half not in d
    assert Float(.5) in d
    assert d[.5] is S.One
    d = sympify(OrderedDict({.5: 1}))
    assert S.Half not in d
    assert Float(.5) in d
    assert d[.5] is S.One
    d = sympify(defaultdict(int, {.5: 1}))
    assert S.Half not in d
    assert Float(.5) in d
    assert d[.5] is S.One

