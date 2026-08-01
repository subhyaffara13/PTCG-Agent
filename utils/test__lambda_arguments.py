
def test_Lambda_arguments():
    raises(TypeError, lambda: Lambda(x, 2*x)(x, y))
    raises(TypeError, lambda: Lambda((x, y), x + y)(x))
    raises(TypeError, lambda: Lambda((), 42)(x))

