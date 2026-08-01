
def test_vector_constraint():
    # gh15514
    def quad(x):
        x = np.asarray(x)
        return [np.sum(x ** 2)]

    nlc = NonlinearConstraint(quad, [2.2], [3])
    oldc = new_constraint_to_old(nlc, np.array([1.0, 1.0]))

    res = shgo(rosen, [(0, 10), (0, 10)], constraints=oldc, sampling_method='sobol')
    assert np.all(np.sum((res.x)**2) >= 2.2)
    assert np.all(np.sum((res.x) ** 2) <= 3.0)
    assert res.success

