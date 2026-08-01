
def test_Integer():
    assert julia_code(Integer(67)) == "67"
    assert julia_code(Integer(-1)) == "-1"


def test_Integer():
    assert maple_code(Integer(67)) == "67"
    assert maple_code(Integer(-1)) == "-1"


def test_Integer():
    assert mcode(Integer(67)) == "67"
    assert mcode(Integer(-1)) == "-1"


def test_Integer():
    assert mcode(Integer(67)) == "67"
    assert mcode(Integer(-1)) == "-1"


def test_Integer():
    sT(Integer(4), "Integer(4)")


def test_Integer():
    assert rust_code(Integer(42)) == "42"
    assert rust_code(Integer(-56)) == "-56"


def test_Integer():
    with _check_warns([_W.WILL_NOT_ASSERT] * 2) as w:
        assert smtlib_code(Integer(67), log_warn=w) == "67"
        assert smtlib_code(Integer(-1), log_warn=w) == "-1"
    with _check_warns([]) as w:
        assert smtlib_code(Integer(67)) == "67"
        assert smtlib_code(Integer(-1)) == "-1"


def test_Integer():
    assert str(Integer(-1)) == "-1"
    assert str(Integer(1)) == "1"
    assert str(Integer(-3)) == "-3"
    assert str(Integer(0)) == "0"
    assert str(Integer(25)) == "25"

