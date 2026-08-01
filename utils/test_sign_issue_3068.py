
def test_sign_issue_3068():
    n = pi**1000
    i = int(n)
    x = Symbol('x')
    assert (n - i).round() == 1  # doesn't hang
    assert sign(n - i) == 1
    # perhaps it's not possible to get the sign right when
    # only 1 digit is being requested for this situation;
    # 2 digits works
    assert (n - x).n(1, subs={x: i}) > 0
    assert (n - x).n(2, subs={x: i}) > 0

