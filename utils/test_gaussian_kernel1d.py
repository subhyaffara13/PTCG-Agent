
def test_gaussian_kernel1d(xp):
    radius = 10
    sigma = 2
    sigma2 = sigma * sigma
    x = np.arange(-radius, radius + 1, dtype=np.float64)
    x = xp.asarray(x)
    phi_x = xp.exp(-0.5 * x * x / sigma2)
    phi_x /= xp.sum(phi_x)
    xp_assert_close(phi_x,
                    xp.asarray(_gaussian_kernel1d(sigma, 0, radius)))
    xp_assert_close(-phi_x * x / sigma2,
                    xp.asarray(_gaussian_kernel1d(sigma, 1, radius)))
    xp_assert_close(phi_x * (x * x / sigma2 - 1) / sigma2,
                    xp.asarray(_gaussian_kernel1d(sigma, 2, radius)))
    xp_assert_close(phi_x * (3 - x * x / sigma2) * x / (sigma2 * sigma2),
                    xp.asarray(_gaussian_kernel1d(sigma, 3, radius)))

