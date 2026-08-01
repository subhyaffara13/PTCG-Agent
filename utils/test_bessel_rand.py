
def test_bessel_rand():
    for f in [besselj, bessely, besseli, besselk, hankel1, hankel2]:
        assert td(f(randcplx(), z), z)

    for f in [jn, yn, hn1, hn2]:
        assert td(f(randint(-10, 10), z), z)

