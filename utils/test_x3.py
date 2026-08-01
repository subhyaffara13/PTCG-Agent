
def test_X3():
    s1 = (sin(x).series()/cos(x).series()).series()
    s2 = tan(x).series()
    assert s2 == x + x**3/3 + 2*x**5/15 + O(x**6)
    assert s1 == s2

