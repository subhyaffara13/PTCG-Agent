
def test_groebner_gcd():
    R, x,y,z = ring("x,y,z", ZZ)

    assert groebner_gcd(x**2 - y**2, x - y) == x - y
    assert groebner_gcd(2*x**2 - 2*y**2, 2*x - 2*y) == 2*x - 2*y

    R, x,y,z = ring("x,y,z", QQ)

    assert groebner_gcd(x**2 - y**2, x - y) == x - y
    assert groebner_gcd(2*x**2 - 2*y**2, 2*x - 2*y) == x - y

