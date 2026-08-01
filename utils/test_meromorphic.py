
def test_meromorphic():
    assert besselj(2, x).is_meromorphic(x, 1) == True
    assert besselj(2, x).is_meromorphic(x, 0) == True
    assert besselj(2, x).is_meromorphic(x, oo) == False
    assert besselj(S(2)/3, x).is_meromorphic(x, 1) == True
    assert besselj(S(2)/3, x).is_meromorphic(x, 0) == False
    assert besselj(S(2)/3, x).is_meromorphic(x, oo) == False
    assert besselj(x, 2*x).is_meromorphic(x, 2) == False
    assert besselk(0, x).is_meromorphic(x, 1) == True
    assert besselk(2, x).is_meromorphic(x, 0) == True
    assert besseli(0, x).is_meromorphic(x, 1) == True
    assert besseli(2, x).is_meromorphic(x, 0) == True
    assert bessely(0, x).is_meromorphic(x, 1) == True
    assert bessely(0, x).is_meromorphic(x, 0) == False
    assert bessely(2, x).is_meromorphic(x, 0) == True
    assert hankel1(3, x**2 + 2*x).is_meromorphic(x, 1) == True
    assert hankel1(0, x).is_meromorphic(x, 0) == False
    assert hankel2(11, 4).is_meromorphic(x, 5) == True
    assert hn1(6, 7*x**3 + 4).is_meromorphic(x, 7) == True
    assert hn2(3, 2*x).is_meromorphic(x, 9) == True
    assert jn(5, 2*x + 7).is_meromorphic(x, 4) == True
    assert yn(8, x**2 + 11).is_meromorphic(x, 6) == True

