
def test_G18():
    assert cf_p(1, 2, 5) == [[1]]
    assert cf_r([[1]]).expand() == S.Half + sqrt(5)/2

