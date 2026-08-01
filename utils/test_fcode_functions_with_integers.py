
def test_fcode_functions_with_integers():
    x= symbols('x')
    log10_17 = log(10).evalf(17)
    loglog10_17 = '0.8340324452479558d0'
    assert fcode(x * log(10)) == "      x*%sd0" % log10_17
    assert fcode(x * log(10)) == "      x*%sd0" % log10_17
    assert fcode(x * log(S(10))) == "      x*%sd0" % log10_17
    assert fcode(log(S(10))) == "      %sd0" % log10_17
    assert fcode(exp(10)) == "      %sd0" % exp(10).evalf(17)
    assert fcode(x * log(log(10))) == "      x*%s" % loglog10_17
    assert fcode(x * log(log(S(10)))) == "      x*%s" % loglog10_17

