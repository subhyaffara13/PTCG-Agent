
def test_violinplot_single_list_quantiles(fig_test, fig_ref):
    # Ensures quantile list for 1D can be passed in as single list
    # First 9 digits of frac(sqrt(83))
    np.random.seed(110433579)
    data = [np.random.normal(size=100)]

    # Test image
    ax = fig_test.subplots()
    ax.violinplot(data, quantiles=[0.1, 0.3, 0.9])

    # Reference image
    ax = fig_ref.subplots()
    ax.violinplot(data, quantiles=[[0.1, 0.3, 0.9]])

