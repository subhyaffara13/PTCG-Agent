
def test_fcode_Relational():
    x, y = symbols("x y")
    assert fcode(Relational(x, y, "=="), source_format="free") == "x == y"
    assert fcode(Relational(x, y, "!="), source_format="free") == "x /= y"
    assert fcode(Relational(x, y, ">="), source_format="free") == "x >= y"
    assert fcode(Relational(x, y, "<="), source_format="free") == "x <= y"
    assert fcode(Relational(x, y, ">"), source_format="free") == "x > y"
    assert fcode(Relational(x, y, "<"), source_format="free") == "x < y"

