
def test_issue_5805():
    arg = ((gamma(x)*hyper((), (), x))*pi)**2
    assert powdenest(arg) == (pi*gamma(x)*hyper((), (), x))**2
    assert arg.is_positive is None

