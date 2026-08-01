
def test_fcode_Xlogical():
    x, y, z = symbols("x y z")
    # binary Xor
    assert fcode(Xor(x, y, evaluate=False), source_format="free") == \
        "x .neqv. y"
    assert fcode(Xor(x, Not(y), evaluate=False), source_format="free") == \
        "x .neqv. .not. y"
    assert fcode(Xor(Not(x), y, evaluate=False), source_format="free") == \
        "y .neqv. .not. x"
    assert fcode(Xor(Not(x), Not(y), evaluate=False),
        source_format="free") == ".not. x .neqv. .not. y"
    assert fcode(Not(Xor(x, y, evaluate=False), evaluate=False),
        source_format="free") == ".not. (x .neqv. y)"
    # binary Equivalent
    assert fcode(Equivalent(x, y), source_format="free") == "x .eqv. y"
    assert fcode(Equivalent(x, Not(y)), source_format="free") == \
        "x .eqv. .not. y"
    assert fcode(Equivalent(Not(x), y), source_format="free") == \
        "y .eqv. .not. x"
    assert fcode(Equivalent(Not(x), Not(y)), source_format="free") == \
        ".not. x .eqv. .not. y"
    assert fcode(Not(Equivalent(x, y), evaluate=False),
        source_format="free") == ".not. (x .eqv. y)"
    # mixed And/Equivalent
    assert fcode(Equivalent(And(y, z), x), source_format="free") == \
        "x .eqv. y .and. z"
    assert fcode(Equivalent(And(z, x), y), source_format="free") == \
        "y .eqv. x .and. z"
    assert fcode(Equivalent(And(x, y), z), source_format="free") == \
        "z .eqv. x .and. y"
    assert fcode(And(Equivalent(y, z), x), source_format="free") == \
        "x .and. (y .eqv. z)"
    assert fcode(And(Equivalent(z, x), y), source_format="free") == \
        "y .and. (x .eqv. z)"
    assert fcode(And(Equivalent(x, y), z), source_format="free") == \
        "z .and. (x .eqv. y)"
    # mixed Or/Equivalent
    assert fcode(Equivalent(Or(y, z), x), source_format="free") == \
        "x .eqv. y .or. z"
    assert fcode(Equivalent(Or(z, x), y), source_format="free") == \
        "y .eqv. x .or. z"
    assert fcode(Equivalent(Or(x, y), z), source_format="free") == \
        "z .eqv. x .or. y"
    assert fcode(Or(Equivalent(y, z), x), source_format="free") == \
        "x .or. (y .eqv. z)"
    assert fcode(Or(Equivalent(z, x), y), source_format="free") == \
        "y .or. (x .eqv. z)"
    assert fcode(Or(Equivalent(x, y), z), source_format="free") == \
        "z .or. (x .eqv. y)"
    # mixed Xor/Equivalent
    assert fcode(Equivalent(Xor(y, z, evaluate=False), x),
        source_format="free") == "x .eqv. (y .neqv. z)"
    assert fcode(Equivalent(Xor(z, x, evaluate=False), y),
        source_format="free") == "y .eqv. (x .neqv. z)"
    assert fcode(Equivalent(Xor(x, y, evaluate=False), z),
        source_format="free") == "z .eqv. (x .neqv. y)"
    assert fcode(Xor(Equivalent(y, z), x, evaluate=False),
        source_format="free") == "x .neqv. (y .eqv. z)"
    assert fcode(Xor(Equivalent(z, x), y, evaluate=False),
        source_format="free") == "y .neqv. (x .eqv. z)"
    assert fcode(Xor(Equivalent(x, y), z, evaluate=False),
        source_format="free") == "z .neqv. (x .eqv. y)"
    # mixed And/Xor
    assert fcode(Xor(And(y, z), x, evaluate=False), source_format="free") == \
        "x .neqv. y .and. z"
    assert fcode(Xor(And(z, x), y, evaluate=False), source_format="free") == \
        "y .neqv. x .and. z"
    assert fcode(Xor(And(x, y), z, evaluate=False), source_format="free") == \
        "z .neqv. x .and. y"
    assert fcode(And(Xor(y, z, evaluate=False), x), source_format="free") == \
        "x .and. (y .neqv. z)"
    assert fcode(And(Xor(z, x, evaluate=False), y), source_format="free") == \
        "y .and. (x .neqv. z)"
    assert fcode(And(Xor(x, y, evaluate=False), z), source_format="free") == \
        "z .and. (x .neqv. y)"
    # mixed Or/Xor
    assert fcode(Xor(Or(y, z), x, evaluate=False), source_format="free") == \
        "x .neqv. y .or. z"
    assert fcode(Xor(Or(z, x), y, evaluate=False), source_format="free") == \
        "y .neqv. x .or. z"
    assert fcode(Xor(Or(x, y), z, evaluate=False), source_format="free") == \
        "z .neqv. x .or. y"
    assert fcode(Or(Xor(y, z, evaluate=False), x), source_format="free") == \
        "x .or. (y .neqv. z)"
    assert fcode(Or(Xor(z, x, evaluate=False), y), source_format="free") == \
        "y .or. (x .neqv. z)"
    assert fcode(Or(Xor(x, y, evaluate=False), z), source_format="free") == \
        "z .or. (x .neqv. y)"
    # trinary Xor
    assert fcode(Xor(x, y, z, evaluate=False), source_format="free") == \
        "x .neqv. y .neqv. z"
    assert fcode(Xor(x, y, Not(z), evaluate=False), source_format="free") == \
        "x .neqv. y .neqv. .not. z"
    assert fcode(Xor(x, Not(y), z, evaluate=False), source_format="free") == \
        "x .neqv. z .neqv. .not. y"
    assert fcode(Xor(Not(x), y, z, evaluate=False), source_format="free") == \
        "y .neqv. z .neqv. .not. x"

