
def test_image_EmptySet():
    x = Symbol('x', real=True)
    assert imageset(x, 2*x, S.EmptySet) == S.EmptySet

