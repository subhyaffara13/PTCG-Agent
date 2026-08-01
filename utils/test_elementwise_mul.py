
def test_elementwise_mul(A):
    assert np.all((A * A).todense() == A.power(2).todense())

