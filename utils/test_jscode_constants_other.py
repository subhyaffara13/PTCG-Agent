
def test_jscode_constants_other():
    assert jscode(
        2*GoldenRatio) == "var GoldenRatio = %s;\n2*GoldenRatio" % GoldenRatio.evalf(17)
    assert jscode(2*Catalan) == "var Catalan = %s;\n2*Catalan" % Catalan.evalf(17)
    assert jscode(
        2*EulerGamma) == "var EulerGamma = %s;\n2*EulerGamma" % EulerGamma.evalf(17)

