
def test_issue_21651():
    k = Symbol('k', positive=True, integer=True)
    exp = 2*2**(-k)
    assert isinstance(floor(exp), floor)


def test_issue_21651():
    k = Symbol('k', positive=True, integer=True)
    exp = 2*2**(-k)
    assert exp.is_integer is None


def test_issue_21651():
    i = Symbol('i')
    a = Sum(floor(2*2**(-i)), (i, S.One, 2))
    assert a.doit() == S.One

