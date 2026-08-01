
def test_minimize_maxiter_noninteger(method):
    # Regression test for gh-23430
    x0 = np.array([1.3, 0.7, 0.8, 1.9, 1.2])
    optimize.minimize(rosen, x0, method=method, options={'maxiter': 100.1})

