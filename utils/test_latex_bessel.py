
def test_latex_bessel():
    from sympy.functions.special.bessel import (besselj, bessely, besseli,
                                                besselk, hankel1, hankel2,
                                                jn, yn, hn1, hn2)
    from sympy.abc import z
    assert latex(besselj(n, z**2)**k) == r'J^{k}_{n}\left(z^{2}\right)'
    assert latex(bessely(n, z)) == r'Y_{n}\left(z\right)'
    assert latex(besseli(n, z)) == r'I_{n}\left(z\right)'
    assert latex(besselk(n, z)) == r'K_{n}\left(z\right)'
    assert latex(hankel1(n, z**2)**2) == \
        r'\left(H^{(1)}_{n}\left(z^{2}\right)\right)^{2}'
    assert latex(hankel2(n, z)) == r'H^{(2)}_{n}\left(z\right)'
    assert latex(jn(n, z)) == r'j_{n}\left(z\right)'
    assert latex(yn(n, z)) == r'y_{n}\left(z\right)'
    assert latex(hn1(n, z)) == r'h^{(1)}_{n}\left(z\right)'
    assert latex(hn2(n, z)) == r'h^{(2)}_{n}\left(z\right)'

