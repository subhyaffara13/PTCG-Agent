
def test_issue_3618():
    assert integrate(pi*sqrt(x), x) == 2*pi*sqrt(x)**3/3
    assert integrate(pi*sqrt(x) + E*sqrt(x)**3, x) == \
        2*pi*sqrt(x)**3/3 + 2*E *sqrt(x)**5/5

