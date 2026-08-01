
def test_Pauli():

    assert sigma1 == sigma1
    assert sigma1 != sigma2

    assert sigma1*sigma2 == I*sigma3
    assert sigma3*sigma1 == I*sigma2
    assert sigma2*sigma3 == I*sigma1

    assert sigma1*sigma1 == 1
    assert sigma2*sigma2 == 1
    assert sigma3*sigma3 == 1

    assert sigma1**0 == 1
    assert sigma1**1 == sigma1
    assert sigma1**2 == 1
    assert sigma1**3 == sigma1
    assert sigma1**4 == 1

    assert sigma3**2 == 1

    assert sigma1*2*sigma1 == 2


def test_Pauli():
    #this and the following test are testing both Pauli and Dirac matrices
    #and also that the general Matrix class works correctly in a real world
    #situation
    sigma1 = msigma(1)
    sigma2 = msigma(2)
    sigma3 = msigma(3)

    assert sigma1 == sigma1
    assert sigma1 != sigma2

    # sigma*I -> I*sigma    (see #354)
    assert sigma1*sigma2 == sigma3*I
    assert sigma3*sigma1 == sigma2*I
    assert sigma2*sigma3 == sigma1*I

    assert sigma1*sigma1 == eye(2)
    assert sigma2*sigma2 == eye(2)
    assert sigma3*sigma3 == eye(2)

    assert sigma1*2*sigma1 == 2*eye(2)
    assert sigma1*sigma3*sigma1 == -sigma3

