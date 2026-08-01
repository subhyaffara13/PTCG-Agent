
def test_TensMul_nocoeff():
    """
    Ensure that for any TensMul instance, self.coeff * self.nocoeff == self
    """

    R3 = TensorIndexType('R3', dim=3)
    i, j = tensor_indices("i j", R3)
    K = TensorHead("K", [R3])
    P = TensorHead("P", [R3])

    expr = TensMul(2, K(i), P(j))
    assert expr.coeff * expr.nocoeff == expr

