
def test_slsqp_segfault_wrong_workspace_computation():
    # See gh-14915
    # This problem is not well-defined, however should not cause a segfault.
    # The previous F77 workspace computation did not handle only equality-
    # constrained problems correctly.
    rng = np.random.default_rng(1742651087222879)
    x = rng.uniform(size=[22,365])
    target = np.linspace(0.9, 4.0, 50)

    def metric(v, weights):
        return [[0, 0],[1, 1]]

    def efficient_metric(v, target):
        def metric_a(weights):
            return metric(v, weights)[1][0]

        def metric_b(weights, v):
            return metric(v, weights)[0][0]

        constraints = ({'type': 'eq', 'fun': lambda x: metric_a(x) - target},
                       {'type': 'eq', 'fun': lambda x: np.sum(x) - 1})
        weights = np.array([len(v)*[1./len(v)]])[0]
        result = minimize(metric_b,
                          weights,
                          args=(v,),
                          method='SLSQP',
                          constraints=constraints)
        return result

    efficient_metric(x, target)

