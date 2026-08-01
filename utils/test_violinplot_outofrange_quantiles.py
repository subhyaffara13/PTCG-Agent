
def test_violinplot_outofrange_quantiles():
    ax = plt.axes()
    # First 9 digits of frac(sqrt(79))
    np.random.seed(888194417)
    data = [np.random.normal(size=100)]

    # Quantile value above 100
    with pytest.raises(ValueError):
        ax.violinplot(data, quantiles=[[0.1, 0.2, 0.3, 1.05]])

    # Quantile value below 0
    with pytest.raises(ValueError):
        ax.violinplot(data, quantiles=[[-0.05, 0.2, 0.3, 0.75]])

