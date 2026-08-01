
def test_ufunc_override(Poly):
    p = Poly([1, 2, 3])
    x = np.ones(3)
    assert_raises(TypeError, np.add, p, x)
    assert_raises(TypeError, np.add, x, p)

