
def test_boxplot_bad_ci():
    x = np.linspace(-7, 7, 140)
    x = np.hstack([-25, x, 25])
    fig, ax = plt.subplots()
    with pytest.raises(ValueError):
        ax.boxplot([x, x], conf_intervals=[[1, 2]])
    with pytest.raises(ValueError):
        ax.boxplot([x, x], conf_intervals=[[1, 2], [1]])

