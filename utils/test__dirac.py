
def test_Dirac():
    gamma0 = mgamma(0)
    gamma1 = mgamma(1)
    gamma2 = mgamma(2)
    gamma3 = mgamma(3)
    gamma5 = mgamma(5)

    # gamma*I -> I*gamma    (see #354)
    assert gamma5 == gamma0 * gamma1 * gamma2 * gamma3 * I
    assert gamma1 * gamma2 + gamma2 * gamma1 == zeros(4)
    assert gamma0 * gamma0 == eye(4) * minkowski_tensor[0, 0]
    assert gamma2 * gamma2 != eye(4) * minkowski_tensor[0, 0]
    assert gamma2 * gamma2 == eye(4) * minkowski_tensor[2, 2]

    assert mgamma(5, True) == \
        mgamma(0, True)*mgamma(1, True)*mgamma(2, True)*mgamma(3, True)*I

