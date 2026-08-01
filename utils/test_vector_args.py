
def test_vector_args():
    raises(ValueError, lambda: BaseVector(3, C))
    raises(TypeError, lambda: BaseVector(0, Vector.zero))

