
def test_latex_integrals():
    assert latex(Integral(log(x), x)) == r"\int \log{\left(x \right)}\, dx"
    assert latex(Integral(x**2, (x, 0, 1))) == \
        r"\int\limits_{0}^{1} x^{2}\, dx"
    assert latex(Integral(x**2, (x, 10, 20))) == \
        r"\int\limits_{10}^{20} x^{2}\, dx"
    assert latex(Integral(y*x**2, (x, 0, 1), y)) == \
        r"\int\int\limits_{0}^{1} x^{2} y\, dx\, dy"
    assert latex(Integral(y*x**2, (x, 0, 1), y), mode='equation*') == \
        r"\begin{equation*}\int\int\limits_{0}^{1} x^{2} y\, dx\, dy\end{equation*}"
    assert latex(Integral(y*x**2, (x, 0, 1), y), mode='equation*', itex=True) \
        == r"$$\int\int_{0}^{1} x^{2} y\, dx\, dy$$"
    assert latex(Integral(x, (x, 0))) == r"\int\limits^{0} x\, dx"
    assert latex(Integral(x*y, x, y)) == r"\iint x y\, dx\, dy"
    assert latex(Integral(x*y*z, x, y, z)) == r"\iiint x y z\, dx\, dy\, dz"
    assert latex(Integral(x*y*z*t, x, y, z, t)) == \
        r"\iiiint t x y z\, dx\, dy\, dz\, dt"
    assert latex(Integral(x, x, x, x, x, x, x)) == \
        r"\int\int\int\int\int\int x\, dx\, dx\, dx\, dx\, dx\, dx"
    assert latex(Integral(x, x, y, (z, 0, 1))) == \
        r"\int\limits_{0}^{1}\int\int x\, dx\, dy\, dz"

    # for negative nested Integral
    assert latex(Integral(-Integral(y**2,x),x)) == \
        r'\int \left(- \int y^{2}\, dx\right)\, dx'
    assert latex(Integral(-Integral(-Integral(y,x),x),x)) == \
        r'\int \left(- \int \left(- \int y\, dx\right)\, dx\right)\, dx'

    # fix issue #10806
    assert latex(Integral(z, z)**2) == r"\left(\int z\, dz\right)^{2}"
    assert latex(Integral(x + z, z)) == r"\int \left(x + z\right)\, dz"
    assert latex(Integral(x+z/2, z)) == \
        r"\int \left(x + \frac{z}{2}\right)\, dz"
    assert latex(Integral(x**y, z)) == r"\int x^{y}\, dz"

    # set diff operator
    assert latex(Integral(x, x), diff_operator="rd") == r'\int x\, \mathrm{d}x'
    assert latex(Integral(x, (x, 0, 1)), diff_operator="rd") == r'\int\limits_{0}^{1} x\, \mathrm{d}x'

