
def test_fcode_precedence():
    x, y = symbols("x y")
    assert fcode(And(x < y, y < x + 1), source_format="free") == \
        "x < y .and. y < x + 1"
    assert fcode(Or(x < y, y < x + 1), source_format="free") == \
        "x < y .or. y < x + 1"
    assert fcode(Xor(x < y, y < x + 1, evaluate=False),
        source_format="free") == "x < y .neqv. y < x + 1"
    assert fcode(Equivalent(x < y, y < x + 1), source_format="free") == \
        "x < y .eqv. y < x + 1"

