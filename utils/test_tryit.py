
def test_tryit():
    def rl(expr: Basic) -> Basic:
        assert False

    safe_rl = tryit(rl, AssertionError)
    assert safe_rl(S(1)) == S(1)

