
def test_print_without_operators():
    assert glsl_code(x*y,use_operators = False) == 'mul(x, y)'
    assert glsl_code(x**y+z,use_operators = False) == 'add(pow(x, y), z)'
    assert glsl_code(x*(y+z),use_operators = False) == 'mul(x, add(y, z))'
    assert glsl_code(x*(y+z),use_operators = False) == 'mul(x, add(y, z))'
    assert glsl_code(x*(y+z**y**0.5),use_operators = False) == 'mul(x, add(y, pow(z, sqrt(y))))'
    assert glsl_code(-x-y, use_operators=False, zero='zero()') == 'sub(zero(), add(x, y))'
    assert glsl_code(-x-y, use_operators=False) == 'sub(0.0, add(x, y))'

