
def test_rand():
    x = numpy.matlib.rand(3)
    # check matrix type, array would have shape (3,)
    assert_(x.ndim == 2)

