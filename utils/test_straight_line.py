
def test_straight_line():
    F = f(x)
    Fd = F.diff(x)
    L = sqrt(1 + Fd**2)
    assert diff(L, F) == 0
    assert diff(L, Fd) == Fd/sqrt(1 + Fd**2)

