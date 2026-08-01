
def test_issue_19114():
    expr = (B & C) | (A & ~C) | (~A & ~B)
    # Expression is minimal, but there are multiple minimal forms possible
    res1 = (A & B) | (C & ~A) | (~B & ~C)
    result = to_dnf(expr, simplify=True)
    assert result in (expr, res1)

