
def test_boxplot_not_single():
    fig, ax = plt.subplots()
    ax.boxplot(np.random.rand(100), positions=[3])
    ax.boxplot(np.random.rand(100), positions=[5])
    fig.canvas.draw()
    assert ax.get_xlim() == (2.5, 5.5)
    assert list(ax.get_xticks()) == [3, 5]
    assert [t.get_text() for t in ax.get_xticklabels()] == ["3", "5"]

