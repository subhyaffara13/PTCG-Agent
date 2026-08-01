
def test_ccode_constants_other():
    assert ccode(2*GoldenRatio) == "const double GoldenRatio = %s;\n2*GoldenRatio" % GoldenRatio.evalf(17)
    assert ccode(
        2*Catalan) == "const double Catalan = %s;\n2*Catalan" % Catalan.evalf(17)
    assert ccode(2*EulerGamma) == "const double EulerGamma = %s;\n2*EulerGamma" % EulerGamma.evalf(17)

