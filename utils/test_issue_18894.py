
def test_issue_18894():
    items = [S(3)/16 + sqrt(3*sqrt(3) + 10)/8, S(1)/8 + 3*sqrt(3)/16, S(1)/8 + 3*sqrt(3)/16, -S(3)/16 + sqrt(3*sqrt(3) + 10)/8]
    R, a = sring(items, extension=True)
    assert R.domain == QQ.algebraic_field(sqrt(3)+sqrt(3*sqrt(3)+10))
    assert R.gens == ()
    result = []
    for item in items:
        result.append(R.domain.from_sympy(item))
    assert a == result

