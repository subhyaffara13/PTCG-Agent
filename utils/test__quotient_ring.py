
def test_QuotientRing():
    from sympy.polys.domains import QQ
    R = QQ.old_poly_ring(x)/[x**2 + 1]

    assert latex(R) == \
        r"\frac{\mathbb{Q}\left[x\right]}{\left\langle {x^{2} + 1} \right\rangle}"
    assert latex(R.one) == r"{1} + {\left\langle {x^{2} + 1} \right\rangle}"


def test_QuotientRing():
    R = QQ.old_poly_ring(x)/[x**2 + 1]

    ucode_str = \
"""\
  ℚ[x]  \n\
────────\n\
╱ 2    ╲\n\
╲x  + 1╱\
"""

    ascii_str = \
"""\
 QQ[x]  \n\
--------\n\
  2     \n\
<x  + 1>\
"""

    assert upretty(R) == ucode_str
    assert pretty(R) == ascii_str

    ucode_str = \
"""\
    ╱ 2    ╲\n\
1 + ╲x  + 1╱\
"""

    ascii_str = \
"""\
      2     \n\
1 + <x  + 1>\
"""

    assert upretty(R.one) == ucode_str
    assert pretty(R.one) == ascii_str


def test_QuotientRing():
    I = QQ.old_poly_ring(x).ideal(x**2 + 1)
    R = QQ.old_poly_ring(x)/I

    assert R == QQ.old_poly_ring(x)/[x**2 + 1]
    assert R == QQ.old_poly_ring(x)/QQ.old_poly_ring(x).ideal(x**2 + 1)
    assert R != QQ.old_poly_ring(x)

    assert R.convert(1)/x == -x + I
    assert -1 + I == x**2 + I
    assert R.convert(ZZ(1), ZZ) == 1 + I
    assert R.convert(R.convert(x), R) == R.convert(x)

    X = R.convert(x)
    Y = QQ.old_poly_ring(x).convert(x)
    assert -1 + I == X**2 + I
    assert -1 + I == Y**2 + I
    assert R.to_sympy(X) == x

    raises(ValueError, lambda: QQ.old_poly_ring(x)/QQ.old_poly_ring(x, y).ideal(x))

    R = QQ.old_poly_ring(x, order="ilex")
    I = R.ideal(x)
    assert R.convert(1) + I == (R/I).convert(1)

