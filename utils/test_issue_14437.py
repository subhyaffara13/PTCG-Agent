
def test_issue_14437():
    f = Function('f')(x, y, z)
    assert integrate(f, (x, 0, 1), (y, 0, 2), (z, 0, 3)) == \
                Integral(f, (x, 0, 1), (y, 0, 2), (z, 0, 3))

