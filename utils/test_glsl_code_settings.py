
def test_glsl_code_settings():
    raises(TypeError, lambda: glsl_code(sin(x), method="garbage"))

