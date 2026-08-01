
def test_Tuple_array_type_custom():
    gl = glsl_code
    A = symbols('a b c')
    assert gl(A, array_type='AbcType', glsl_types=False) == 'AbcType[3](a, b, c)'

