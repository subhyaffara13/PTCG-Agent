
def test_legend_inverse_size_label_relationship():
    """
    Ensure legend markers scale appropriately when label and size are
    inversely related.
    Here label = 5 / size
    """

    np.random.seed(19680801)
    X = np.random.random(50)
    Y = np.random.random(50)
    C = 1 - np.random.random(50)
    S = 5 / C

    legend_sizes = [0.2, 0.4, 0.6, 0.8]
    fig, ax = plt.subplots()
    sc = ax.scatter(X, Y, s=S)
    handles, labels = sc.legend_elements(
      prop='sizes', num=legend_sizes, func=lambda s: 5 / s
    )

    # Convert markersize scale to 's' scale
    handle_sizes = [x.get_markersize() for x in handles]
    handle_sizes = [5 / x**2 for x in handle_sizes]

    assert_array_almost_equal(handle_sizes, legend_sizes, decimal=1)

