
def test_glsl_code_sqrt():
    assert glsl_code(sqrt(x)) == "sqrt(x)"
    assert glsl_code(x**0.5) == "sqrt(x)"
    assert glsl_code(sqrt(x)) == "sqrt(x)"

