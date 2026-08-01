
def test_random_state_property():
    scale = np.eye(3)
    scale[0, 1] = 0.5
    scale[1, 0] = 0.5
    dists = [
        [multivariate_normal, ()],
        [dirichlet, (np.array([1.]), )],
        [wishart, (10, scale)],
        [invwishart, (10, scale)],
        [multinomial, (5, [0.5, 0.4, 0.1])],
        [ortho_group, (2,)],
        [special_ortho_group, (2,)]
    ]
    for distfn, args in dists:
        check_random_state_property(distfn, args)
        check_pickling(distfn, args)

