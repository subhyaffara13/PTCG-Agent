
def test_trust_constr():
    def quad(x):
        x = np.asarray(x)
        return [np.sum(x ** 2)]

    nlc = NonlinearConstraint(quad, [2.6], [3])
    minimizer_kwargs = {'method': 'trust-constr'}
    # note that we don't supply the constraints in minimizer_kwargs,
    # so if the final result obeys the constraints we know that shgo
    # passed them on to 'trust-constr'
    res = shgo(
        rosen,
        [(0, 10), (0, 10)],
        constraints=nlc,
        sampling_method='sobol',
        minimizer_kwargs=minimizer_kwargs
    )
    assert np.all(np.sum((res.x)**2) >= 2.6)
    assert np.all(np.sum((res.x) ** 2) <= 3.0)
    assert res.success

