
def test_fcode_Logical():
    x, y, z = symbols("x y z")
    # unary Not
    assert fcode(Not(x), source_format="free") == ".not. x"
    # binary And
    assert fcode(And(x, y), source_format="free") == "x .and. y"
    assert fcode(And(x, Not(y)), source_format="free") == "x .and. .not. y"
    assert fcode(And(Not(x), y), source_format="free") == "y .and. .not. x"
    assert fcode(And(Not(x), Not(y)), source_format="free") == \
        ".not. x .and. .not. y"
    assert fcode(Not(And(x, y), evaluate=False), source_format="free") == \
        ".not. (x .and. y)"
    # binary Or
    assert fcode(Or(x, y), source_format="free") == "x .or. y"
    assert fcode(Or(x, Not(y)), source_format="free") == "x .or. .not. y"
    assert fcode(Or(Not(x), y), source_format="free") == "y .or. .not. x"
    assert fcode(Or(Not(x), Not(y)), source_format="free") == \
        ".not. x .or. .not. y"
    assert fcode(Not(Or(x, y), evaluate=False), source_format="free") == \
        ".not. (x .or. y)"
    # mixed And/Or
    assert fcode(And(Or(y, z), x), source_format="free") == "x .and. (y .or. z)"
    assert fcode(And(Or(z, x), y), source_format="free") == "y .and. (x .or. z)"
    assert fcode(And(Or(x, y), z), source_format="free") == "z .and. (x .or. y)"
    assert fcode(Or(And(y, z), x), source_format="free") == "x .or. y .and. z"
    assert fcode(Or(And(z, x), y), source_format="free") == "y .or. x .and. z"
    assert fcode(Or(And(x, y), z), source_format="free") == "z .or. x .and. y"
    # trinary And
    assert fcode(And(x, y, z), source_format="free") == "x .and. y .and. z"
    assert fcode(And(x, y, Not(z)), source_format="free") == \
        "x .and. y .and. .not. z"
    assert fcode(And(x, Not(y), z), source_format="free") == \
        "x .and. z .and. .not. y"
    assert fcode(And(Not(x), y, z), source_format="free") == \
        "y .and. z .and. .not. x"
    assert fcode(Not(And(x, y, z), evaluate=False), source_format="free") == \
        ".not. (x .and. y .and. z)"
    # trinary Or
    assert fcode(Or(x, y, z), source_format="free") == "x .or. y .or. z"
    assert fcode(Or(x, y, Not(z)), source_format="free") == \
        "x .or. y .or. .not. z"
    assert fcode(Or(x, Not(y), z), source_format="free") == \
        "x .or. z .or. .not. y"
    assert fcode(Or(Not(x), y, z), source_format="free") == \
        "y .or. z .or. .not. x"
    assert fcode(Not(Or(x, y, z), evaluate=False), source_format="free") == \
        ".not. (x .or. y .or. z)"

