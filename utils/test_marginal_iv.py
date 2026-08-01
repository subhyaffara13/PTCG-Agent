
def test_marginal_iv():
    # test input validation
    rng = np.random.default_rng(6111799263660870475)
    n_data = 30
    n_dim = 4
    dataset = rng.normal(size=(n_dim, n_data))
    points = rng.normal(size=(n_dim, 3))

    kde = stats.gaussian_kde(dataset)

    # check that positive and negative indices are equivalent
    dimensions1 = [-1, 1]
    marginal1 = kde.marginal(dimensions1)
    pdf1 = marginal1.pdf(points[dimensions1])

    dimensions2 = [3, -3]
    marginal2 = kde.marginal(dimensions2)
    pdf2 = marginal2.pdf(points[dimensions2])

    assert_equal(pdf1, pdf2)

    # IV for non-integer dimensions
    message = "Elements of `dimensions` must be integers..."
    with pytest.raises(ValueError, match=message):
        kde.marginal([1, 2.5])

    # IV for uniqueness
    message = "All elements of `dimensions` must be unique."
    with pytest.raises(ValueError, match=message):
        kde.marginal([1, 2, 2])

    # IV for non-integer dimensions
    message = (r"Dimensions \[-5  6\] are invalid for a distribution in 4...")
    with pytest.raises(ValueError, match=message):
        kde.marginal([1, -5, 6])

