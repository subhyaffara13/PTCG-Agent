from typing import Tuple

def test_glsl_code_list_tuple_Tuple():
    assert glsl_code([1,2,3,4]) == 'vec4(1, 2, 3, 4)'
    assert glsl_code([1,2,3],glsl_types=False) == 'float[3](1, 2, 3)'
    assert glsl_code([1,2,3]) == glsl_code((1,2,3))
    assert glsl_code([1,2,3]) == glsl_code(Tuple(1,2,3))

    m = MatrixSymbol('A',3,4)
    assert glsl_code([m[0],m[1]])

