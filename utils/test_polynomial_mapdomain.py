
def test_polynomial_mapdomain():
    # test that polynomial preserved matrix subtype.
    # 2018-04-29: moved here from polynomial.tests.polyutils.
    dom1 = [0, 4]
    dom2 = [1, 3]
    x = np.matrix([dom1, dom1])
    res = np.polynomial.polyutils.mapdomain(x, dom1, dom2)
    assert_(isinstance(res, np.matrix))

