
def test_issue_10972_TensMul_data():
    with warns_deprecated_sympy():
        Lorentz = TensorIndexType('Lorentz', metric_symmetry=1, dummy_name='i', dim=2)
        Lorentz.data = [-1, 1]

        mu, nu, alpha, beta = tensor_indices('\\mu, \\nu, \\alpha, \\beta',
                                             Lorentz)

        u = TensorHead('u', [Lorentz])
        u.data = [1, 0]

        F = TensorHead('F', [Lorentz]*2, TensorSymmetry.fully_symmetric(-2))
        F.data = [[0, 1],
                  [-1, 0]]

        mul_1 = F(mu, alpha) * u(-alpha) * F(nu, beta) * u(-beta)
        assert (mul_1.data == Array([[0, 0], [0, 1]]))

        mul_2 = F(mu, alpha) * F(nu, beta) * u(-alpha) * u(-beta)
        assert (mul_2.data == mul_1.data)

        assert ((mul_1 + mul_1).data == 2 * mul_1.data)

