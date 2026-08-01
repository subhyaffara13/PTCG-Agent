
def test_1xN_vecs():
    gl = glsl_code
    for i in range(1,10):
        A = Matrix(range(i))
        assert gl(A.transpose()) == gl(A)
        assert gl(A,mat_transpose=True) == gl(A)
        if i > 1:
            if i <= 4:
                assert gl(A) == 'vec%s(%s)' % (i,', '.join(str(s) for s in range(i)))
            else:
                assert gl(A) == 'float[%s](%s)' % (i,', '.join(str(s) for s in range(i)))

