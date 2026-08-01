
def test_jscode_functions():
    assert jscode(sin(x) ** cos(x)) == "Math.pow(Math.sin(x), Math.cos(x))"
    assert jscode(sinh(x) * cosh(x)) == "Math.sinh(x)*Math.cosh(x)"
    assert jscode(Max(x, y) + Min(x, y)) == "Math.max(x, y) + Math.min(x, y)"
    assert jscode(tanh(x)*acosh(y)) == "Math.tanh(x)*Math.acosh(y)"
    assert jscode(asin(x)-acos(y)) == "-Math.acos(y) + Math.asin(x)"

