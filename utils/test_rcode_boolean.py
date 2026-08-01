
def test_rcode_boolean():
    assert rcode(True) == "True"
    assert rcode(S.true) == "True"
    assert rcode(False) == "False"
    assert rcode(S.false) == "False"
    assert rcode(x & y) == "x & y"
    assert rcode(x | y) == "x | y"
    assert rcode(~x) == "!x"
    assert rcode(x & y & z) == "x & y & z"
    assert rcode(x | y | z) == "x | y | z"
    assert rcode((x & y) | z) == "z | x & y"
    assert rcode((x | y) & z) == "z & (x | y)"

