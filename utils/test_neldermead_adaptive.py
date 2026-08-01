
def test_neldermead_adaptive():
    def func(x):
        return np.sum(x ** 2)
    p0 = [0.15746215, 0.48087031, 0.44519198, 0.4223638, 0.61505159,
          0.32308456, 0.9692297, 0.4471682, 0.77411992, 0.80441652,
          0.35994957, 0.75487856, 0.99973421, 0.65063887, 0.09626474]

    res = optimize.minimize(func, p0, method='Nelder-Mead')
    assert_equal(res.success, False)

    res = optimize.minimize(func, p0, method='Nelder-Mead',
                            options={'adaptive': True})
    assert_equal(res.success, True)

