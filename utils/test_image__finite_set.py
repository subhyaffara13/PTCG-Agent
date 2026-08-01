
def test_image_FiniteSet():
    x = Symbol('x', real=True)
    assert imageset(x, 2*x, FiniteSet(1, 2, 3)) == FiniteSet(2, 4, 6)

