
def test_violinplot_bad_positions():
    ax = plt.axes()
    # First 9 digits of frac(sqrt(47))
    np.random.seed(855654600)
    data = [np.random.normal(size=100) for _ in range(4)]
    with pytest.raises(ValueError):
        ax.violinplot(data, positions=range(5))

