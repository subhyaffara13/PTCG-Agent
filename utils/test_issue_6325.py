
def test_issue_6325():
    ans = (b**2 + z**2 - (b*(a + b*t) + z*(c + t*z))**2/(
        (a + b*t)**2 + (c + t*z)**2))/sqrt((a + b*t)**2 + (c + t*z)**2)
    e = sqrt((a + b*t)**2 + (c + z*t)**2)
    assert diff(e, t, 2) == ans
    assert e.diff(t, 2) == ans
    assert diff(e, t, 2, simplify=False) != ans

