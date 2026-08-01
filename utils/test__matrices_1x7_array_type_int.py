
def test_Matrices_1x7_array_type_int():
    gl = glsl_code
    A = Matrix([1,2,3,4,5,6,7])
    assert gl(A, array_type='int') == 'int[7](1, 2, 3, 4, 5, 6, 7)'

