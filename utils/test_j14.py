
def test_J14():
    p = hyper([S.Half, S.Half], [R(3, 2)], z**2)
    assert hyperexpand(p) == asin(z)/z

