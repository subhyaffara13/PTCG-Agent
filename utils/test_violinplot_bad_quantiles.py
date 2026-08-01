
def test_violinplot_bad_quantiles():
    ax = plt.axes()
    # First 9 digits of frac(sqrt(73))
    np.random.seed(544003745)
    data = [np.random.normal(size=100)]

    # Different size quantile list and plots
    with pytest.raises(ValueError):
        ax.violinplot(data, quantiles=[[0.1, 0.2], [0.5, 0.7]])

