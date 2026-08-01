
def test_rcode_constants_other():
    assert rcode(2*GoldenRatio) == "GoldenRatio = 1.61803398874989;\n2*GoldenRatio"
    assert rcode(
        2*Catalan) == "Catalan = 0.915965594177219;\n2*Catalan"
    assert rcode(2*EulerGamma) == "EulerGamma = 0.577215664901533;\n2*EulerGamma"

