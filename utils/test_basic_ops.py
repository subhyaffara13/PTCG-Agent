
def test_basic_ops():
    assert julia_code(x*y) == "x .* y"
    assert julia_code(x + y) == "x + y"
    assert julia_code(x - y) == "x - y"
    assert julia_code(-x) == "-x"


def test_basic_ops():
    assert maple_code(x * y) == "x*y"
    assert maple_code(x + y) == "x + y"
    assert maple_code(x - y) == "x - y"
    assert maple_code(-x) == "-x"


def test_basic_ops():
    assert mcode(x*y) == "x.*y"
    assert mcode(x + y) == "x + y"
    assert mcode(x - y) == "x - y"
    assert mcode(-x) == "-x"


def test_basic_ops():
    assert rust_code(x + y) == "x + y"
    assert rust_code(x - y) == "x - y"
    assert rust_code(x * y) == "x*y"
    assert rust_code(x / y) == "x*y.recip()"
    assert rust_code(-x) == "-x"
    assert rust_code(2 * x) == "2.0*x"
    assert rust_code(y + 2) == "y + 2.0"
    assert rust_code(x + n) == "n as f64 + x"


def test_basic_ops():
    with _check_warns([_W.DEFAULTING_TO_FLOAT, _W.DEFAULTING_TO_FLOAT, _W.WILL_NOT_ASSERT]) as w:
        assert smtlib_code(x * y, auto_declare=False, log_warn=w) == "(* x y)"

    with _check_warns([_W.DEFAULTING_TO_FLOAT, _W.DEFAULTING_TO_FLOAT, _W.WILL_NOT_ASSERT]) as w:
        assert smtlib_code(x + y, auto_declare=False, log_warn=w) == "(+ x y)"

    # with _check_warns([_SmtlibWarnings.DEFAULTING_TO_FLOAT, _SmtlibWarnings.DEFAULTING_TO_FLOAT, _SmtlibWarnings.WILL_NOT_ASSERT]) as w:
    # todo: implement re-write, currently does '(+ x (* -1 y))' instead
    # assert smtlib_code(x - y, auto_declare=False, log_warn=w) == "(- x y)"

    with _check_warns([_W.DEFAULTING_TO_FLOAT, _W.WILL_NOT_ASSERT]) as w:
        assert smtlib_code(-x, auto_declare=False, log_warn=w) == "(* -1 x)"

