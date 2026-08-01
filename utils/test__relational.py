
def test_Relational():
    assert jscode(Eq(x, y)) == "x == y"
    assert jscode(Ne(x, y)) == "x != y"
    assert jscode(Le(x, y)) == "x <= y"
    assert jscode(Lt(x, y)) == "x < y"
    assert jscode(Gt(x, y)) == "x > y"
    assert jscode(Ge(x, y)) == "x >= y"


def test_Relational():
    assert julia_code(Eq(x, y)) == "x == y"
    assert julia_code(Ne(x, y)) == "x != y"
    assert julia_code(Le(x, y)) == "x <= y"
    assert julia_code(Lt(x, y)) == "x < y"
    assert julia_code(Gt(x, y)) == "x > y"
    assert julia_code(Ge(x, y)) == "x >= y"


def test_Relational():
    assert maple_code(Eq(x, y)) == "x = y"
    assert maple_code(Ne(x, y)) == "x <> y"
    assert maple_code(Le(x, y)) == "x <= y"
    assert maple_code(Lt(x, y)) == "x < y"
    assert maple_code(Gt(x, y)) == "x > y"
    assert maple_code(Ge(x, y)) == "x >= y"


def test_Relational():
    assert mcode(Eq(x, y)) == "x == y"
    assert mcode(Ne(x, y)) == "x != y"
    assert mcode(Le(x, y)) == "x <= y"
    assert mcode(Lt(x, y)) == "x < y"
    assert mcode(Gt(x, y)) == "x > y"
    assert mcode(Ge(x, y)) == "x >= y"


def test_Relational():
    assert mcode(Eq(x, y)) == "x == y"
    assert mcode(Ne(x, y)) == "x != y"
    assert mcode(Le(x, y)) == "x <= y"
    assert mcode(Lt(x, y)) == "x < y"
    assert mcode(Gt(x, y)) == "x > y"
    assert mcode(Ge(x, y)) == "x >= y"


def test_Relational():
    assert precedence(Rel(x + y, y, "<")) == PRECEDENCE["Relational"]


def test_Relational():
    assert rust_code(Eq(x, y)) == "x == y"
    assert rust_code(Ne(x, y)) == "x != y"
    assert rust_code(Le(x, y)) == "x <= y"
    assert rust_code(Lt(x, y)) == "x < y"
    assert rust_code(Gt(x, y)) == "x > y"
    assert rust_code(Ge(x, y)) == "x >= y"


def test_Relational():
    with _check_warns([_W.DEFAULTING_TO_FLOAT] * 12) as w:
        assert smtlib_code(Eq(x, y), auto_declare=False, log_warn=w) == "(assert (= x y))"
        assert smtlib_code(Ne(x, y), auto_declare=False, log_warn=w) == "(assert (not (= x y)))"
        assert smtlib_code(Le(x, y), auto_declare=False, log_warn=w) == "(assert (<= x y))"
        assert smtlib_code(Lt(x, y), auto_declare=False, log_warn=w) == "(assert (< x y))"
        assert smtlib_code(Gt(x, y), auto_declare=False, log_warn=w) == "(assert (> x y))"
        assert smtlib_code(Ge(x, y), auto_declare=False, log_warn=w) == "(assert (>= x y))"


def test_Relational():
    assert str(Rel(x, y, "<")) == "x < y"
    assert str(Rel(x + y, y, "==")) == "Eq(x + y, y)"
    assert str(Rel(x, y, "!=")) == "Ne(x, y)"
    assert str(Eq(x, 1) | Eq(x, 2)) == "Eq(x, 1) | Eq(x, 2)"
    assert str(Ne(x, 1) & Ne(x, 2)) == "Ne(x, 1) & Ne(x, 2)"

