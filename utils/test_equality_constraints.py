
def test_equality_constraints():
    # gh16260
    bounds = [(0.9, 4.0)] * 2  # Constrain probabilities to 0 and 1.

    def faulty(x):
        return x[0] + x[1]

    nlc = NonlinearConstraint(faulty, 3.9, 3.9)
    res = shgo(rosen, bounds=bounds, constraints=nlc)
    assert_allclose(np.sum(res.x), 3.9)

    def faulty(x):
        return x[0] + x[1] - 3.9

    constraints = {'type': 'eq', 'fun': faulty}
    res = shgo(rosen, bounds=bounds, constraints=constraints)
    assert_allclose(np.sum(res.x), 3.9)

    bounds = [(0, 1.0)] * 4
    # sum of variable should equal 1.
    def faulty(x):
        return x[0] + x[1] + x[2] + x[3] - 1

    # options = {'minimize_every_iter': True, 'local_iter':10}
    constraints = {'type': 'eq', 'fun': faulty}
    res = shgo(
        lambda x: - np.prod(x),
        bounds=bounds,
        constraints=constraints,
        sampling_method='sobol'
    )
    assert_allclose(np.sum(res.x), 1.0)

