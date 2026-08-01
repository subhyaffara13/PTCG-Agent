
def test_glsl_code_Relational():
    assert glsl_code(Eq(x, y)) == "x == y"
    assert glsl_code(Ne(x, y)) == "x != y"
    assert glsl_code(Le(x, y)) == "x <= y"
    assert glsl_code(Lt(x, y)) == "x < y"
    assert glsl_code(Gt(x, y)) == "x > y"
    assert glsl_code(Ge(x, y)) == "x >= y"

