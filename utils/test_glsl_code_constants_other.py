
def test_glsl_code_constants_other():
    assert glsl_code(2*GoldenRatio) == "float GoldenRatio = 1.61803399;\n2*GoldenRatio"
    assert glsl_code(2*Catalan) == "float Catalan = 0.915965594;\n2*Catalan"
    assert glsl_code(2*EulerGamma) == "float EulerGamma = 0.577215665;\n2*EulerGamma"

