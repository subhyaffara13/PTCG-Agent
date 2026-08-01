
def test_Matrices_1x7():
    gl = glsl_code
    A = Matrix([1,2,3,4,5,6,7])
    assert gl(A) == 'float[7](1, 2, 3, 4, 5, 6, 7)'
    assert gl(A.transpose()) == 'float[7](1, 2, 3, 4, 5, 6, 7)'

