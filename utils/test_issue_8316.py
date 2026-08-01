
def test_issue_8316():
    f = Poly(7*x**8 - 9)
    assert len(f.all_roots()) == 8
    f = Poly(7*x**8 - 10)
    assert len(f.all_roots()) == 8

