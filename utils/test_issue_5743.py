
def test_issue_5743():
    assert (x*sqrt(
        x + y)*(1 + sqrt(x + y))).expand() == x**2 + x*y + x*sqrt(x + y)
    assert (x*sqrt(
        x + y)*(1 + x*sqrt(x + y))).expand() == x**3 + x**2*y + x*sqrt(x + y)

