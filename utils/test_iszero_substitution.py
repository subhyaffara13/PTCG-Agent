
def test_iszero_substitution():
    """ When doing numerical computations, all elements that pass
    the iszerofunc test should be set to numerically zero if they
    aren't already. """

    # Matrix from issue #9060
    m = Matrix([[0.9, -0.1, -0.2, 0],[-0.8, 0.9, -0.4, 0],[-0.1, -0.8, 0.6, 0]])
    m_rref = m.rref(iszerofunc=lambda x: abs(x)<6e-15)[0]
    m_correct = Matrix([[1.0,   0, -0.301369863013699, 0],[  0, 1.0, -0.712328767123288, 0],[  0,   0,                  0, 0]])
    m_diff = m_rref - m_correct
    assert m_diff.norm() < 1e-15
    # if a zero-substitution wasn't made, this entry will be -1.11022302462516e-16
    assert m_rref[2,2] == 0


def test_iszero_substitution():
    """ When doing numerical computations, all elements that pass
    the iszerofunc test should be set to numerically zero if they
    aren't already. """

    # Matrix from issue #9060
    m = Matrix([[0.9, -0.1, -0.2, 0],[-0.8, 0.9, -0.4, 0],[-0.1, -0.8, 0.6, 0]])
    m_rref = m.rref(iszerofunc=lambda x: abs(x)<6e-15)[0]
    m_correct = Matrix([[1.0,   0, -0.301369863013699, 0],[  0, 1.0, -0.712328767123288, 0],[  0,   0,                  0, 0]])
    m_diff = m_rref - m_correct
    assert m_diff.norm() < 1e-15
    # if a zero-substitution wasn't made, this entry will be -1.11022302462516e-16
    assert m_rref[2,2] == 0

