
def test_smtlib_boolean():
    with _check_warns([]) as w:
        assert smtlib_code(True, auto_assert=False, log_warn=w) == 'true'
        assert smtlib_code(True, log_warn=w) == '(assert true)'
        assert smtlib_code(S.true, log_warn=w) == '(assert true)'
        assert smtlib_code(S.false, log_warn=w) == '(assert false)'
        assert smtlib_code(False, log_warn=w) == '(assert false)'
        assert smtlib_code(False, auto_assert=False, log_warn=w) == 'false'

