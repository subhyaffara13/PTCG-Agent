
def test_expand_radicals():
    a = (x + y)**R(1, 2)

    assert (a**1).expand() == a
    assert (a**3).expand() == x*a + y*a
    assert (a**5).expand() == x**2*a + 2*x*y*a + y**2*a

    assert (1/a**1).expand() == 1/a
    assert (1/a**3).expand() == 1/(x*a + y*a)
    assert (1/a**5).expand() == 1/(x**2*a + 2*x*y*a + y**2*a)

    a = (x + y)**R(1, 3)

    assert (a**1).expand() == a
    assert (a**2).expand() == a**2
    assert (a**4).expand() == x*a + y*a
    assert (a**5).expand() == x*a**2 + y*a**2
    assert (a**7).expand() == x**2*a + 2*x*y*a + y**2*a

