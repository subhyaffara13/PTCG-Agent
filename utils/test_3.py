
def test_3():

    def todense_old_impl(self):
        s, y, n_corrs, rho = self.sk, self.yk, self.n_corrs, self.rho
        I_arr = np.eye(*self.shape, dtype=self.dtype)
        Hk = I_arr

        for i in range(n_corrs):
            A1 = I_arr - s[i][:, np.newaxis] * y[i][np.newaxis, :] * rho[i]
            A2 = I_arr - y[i][:, np.newaxis] * s[i][np.newaxis, :] * rho[i]

            Hk = np.dot(A1, np.dot(Hk, A2)) + (rho[i] * s[i][:, np.newaxis] *
                                                        s[i][np.newaxis, :])
        return Hk

    H0 = [[3, 0], [1, 2]]

    def f(x):
        return np.dot(x, np.dot(scipy.linalg.inv(H0), x))

    result1 = minimize(fun=f, method='L-BFGS-B', x0=[10, 20])
    assert_allclose(result1.hess_inv.todense(), todense_old_impl(result1.hess_inv))

