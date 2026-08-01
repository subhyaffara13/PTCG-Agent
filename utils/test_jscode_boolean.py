
def test_jscode_boolean():
    assert jscode(x & y) == "x && y"
    assert jscode(x | y) == "x || y"
    assert jscode(~x) == "!x"
    assert jscode(x & y & z) == "x && y && z"
    assert jscode(x | y | z) == "x || y || z"
    assert jscode((x & y) | z) == "z || x && y"
    assert jscode((x | y) & z) == "z && (x || y)"

