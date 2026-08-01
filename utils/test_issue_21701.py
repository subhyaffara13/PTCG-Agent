
def test_issue_21701():
    assert limit((besselj(z, x)/x**z).subs(z, 7), x, 0) == S(1)/645120

