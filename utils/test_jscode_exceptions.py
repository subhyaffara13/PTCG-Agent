
def test_jscode_exceptions():
    assert jscode(ceiling(x)) == "Math.ceil(x)"
    assert jscode(Abs(x)) == "Math.abs(x)"

