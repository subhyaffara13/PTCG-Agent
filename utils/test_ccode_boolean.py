
def test_ccode_boolean():
    assert ccode(True) == "true"
    assert ccode(S.true) == "true"
    assert ccode(False) == "false"
    assert ccode(S.false) == "false"
    assert ccode(x & y) == "x && y"
    assert ccode(x | y) == "x || y"
    assert ccode(~x) == "!x"
    assert ccode(x & y & z) == "x && y && z"
    assert ccode(x | y | z) == "x || y || z"
    assert ccode((x & y) | z) == "z || x && y"
    assert ccode((x | y) & z) == "z && (x || y)"
    # Automatic rewrites
    assert ccode(x ^ y) == '(x || y) && (!x || !y)'
    assert ccode((x ^ y) ^ z) == '(x || y || z) && (x || !y || !z) && (y || !x || !z) && (z || !x || !y)'
    assert ccode(Implies(x, y)) == 'y || !x'
    assert ccode(Equivalent(x, z ^ y, Implies(z, x))) == '(x || (y || !z) && (z || !y)) && (z && !x || (y || z) && (!y || !z))'

