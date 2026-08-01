
def test_difference_delta__Pow():
    e = 4**n
    assert dd(e, n) == 3*4**n
    assert dd(e, n, 2) == 15*4**n

    e = 4**(2*n)
    assert dd(e, n) == 15*4**(2*n)
    assert dd(e, n, 2) == 255*4**(2*n)

    e = n**4
    assert dd(e, n) == (n + 1)**4 - n**4

    e = n**n
    assert dd(e, n) == (n + 1)**(n + 1) - n**n

