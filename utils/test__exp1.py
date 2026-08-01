
def test_Exp1():
    """
    Test that exp(1) prints without error and evaluates close to SymPy's E
    """
    # sy.exp(1) should yield same instance of E as sy.E (singleton), but extra
    # check added for sanity
    e_a = sy.exp(1)
    e_b = sy.E

    np.testing.assert_allclose(float(e_a), np.e)
    np.testing.assert_allclose(float(e_b), np.e)

    e = theano_code_(e_a)
    np.testing.assert_allclose(float(e_a), e.eval())

    e = theano_code_(e_b)
    np.testing.assert_allclose(float(e_b), e.eval())

