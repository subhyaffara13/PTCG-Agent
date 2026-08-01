
def test_besseli_leading_term():
    assert besseli(0, x).as_leading_term(x) == 1
    assert besseli(1, sin(x)).as_leading_term(x) == x/2
    assert besseli(1, 2*sqrt(x)).as_leading_term(x) == sqrt(x)

