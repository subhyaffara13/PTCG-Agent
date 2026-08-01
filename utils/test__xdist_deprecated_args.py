
def test_Xdist_deprecated_args(metric):
    # testing both cdist and pdist deprecated warnings
    X1 = np.asarray([[1., 2., 3.],
                     [1.2, 2.3, 3.4],
                     [2.2, 2.3, 4.4],
                     [22.2, 23.3, 44.4]])

    with pytest.raises(TypeError):
        cdist(X1, X1, metric, 2.)

    with pytest.raises(TypeError):
        pdist(X1, metric, 2.)

    for arg in ["p", "V", "VI"]:
        kwargs = {arg: np.asarray(1.)}

        if ((arg == "V" and metric == "seuclidean")
                or (arg == "VI" and metric == "mahalanobis")
                or (arg == "p" and metric == "minkowski")):
            continue

        with pytest.raises(TypeError):
            cdist(X1, X1, metric, **kwargs)

        with pytest.raises(TypeError):
            pdist(X1, metric, **kwargs)

