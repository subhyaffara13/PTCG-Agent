
def test_pretty_Domain():
    expr = FF(23)

    assert pretty(expr) == "GF(23)"
    assert upretty(expr) == "ℤ₂₃"

    expr = ZZ

    assert pretty(expr) == "ZZ"
    assert upretty(expr) == "ℤ"

    expr = QQ

    assert pretty(expr) == "QQ"
    assert upretty(expr) == "ℚ"

    expr = RR

    assert pretty(expr) == "RR"
    assert upretty(expr) == "ℝ"

    expr = QQ[x]

    assert pretty(expr) == "QQ[x]"
    assert upretty(expr) == "ℚ[x]"

    expr = QQ[x, y]

    assert pretty(expr) == "QQ[x, y]"
    assert upretty(expr) == "ℚ[x, y]"

    expr = ZZ.frac_field(x)

    assert pretty(expr) == "ZZ(x)"
    assert upretty(expr) == "ℤ(x)"

    expr = ZZ.frac_field(x, y)

    assert pretty(expr) == "ZZ(x, y)"
    assert upretty(expr) == "ℤ(x, y)"

    expr = QQ.poly_ring(x, y, order=grlex)

    assert pretty(expr) == "QQ[x, y, order=grlex]"
    assert upretty(expr) == "ℚ[x, y, order=grlex]"

    expr = QQ.poly_ring(x, y, order=ilex)

    assert pretty(expr) == "QQ[x, y, order=ilex]"
    assert upretty(expr) == "ℚ[x, y, order=ilex]"

