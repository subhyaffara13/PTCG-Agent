
def test_constants_other():
    assert julia_code(2*GoldenRatio) == "2 * golden"
    assert julia_code(2*Catalan) == "2 * catalan"
    assert julia_code(2*EulerGamma) == "2 * eulergamma"


def test_constants_other():
    assert maple_code(2 * GoldenRatio) == '2*(1/2 + (1/2)*sqrt(5))'
    assert maple_code(2 * Catalan) == '2*Catalan'
    assert maple_code(2 * EulerGamma) == "2*gamma"


def test_constants_other():
    assert mcode(2*GoldenRatio) == "2*(1+sqrt(5))/2"
    assert mcode(2*Catalan) == "2*%s" % Catalan.evalf(17)
    assert mcode(2*EulerGamma) == "2*%s" % EulerGamma.evalf(17)


def test_constants_other():
    assert rust_code(2*GoldenRatio) == "const GoldenRatio: f64 = %s;\n2.0*GoldenRatio" % GoldenRatio.evalf(17)
    assert rust_code(
            2*Catalan) == "const Catalan: f64 = %s;\n2.0*Catalan" % Catalan.evalf(17)
    assert rust_code(2*EulerGamma) == "const EulerGamma: f64 = %s;\n2.0*EulerGamma" % EulerGamma.evalf(17)

