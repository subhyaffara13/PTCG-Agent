
def test_boxplot_bad_medians():
    x = np.linspace(-7, 7, 140)
    x = np.hstack([-25, x, 25])
    fig, ax = plt.subplots()
    with pytest.raises(ValueError):
        ax.boxplot(x, usermedians=[1, 2])
    with pytest.raises(ValueError):
        ax.boxplot([x, x], usermedians=[[1, 2], [1, 2]])

