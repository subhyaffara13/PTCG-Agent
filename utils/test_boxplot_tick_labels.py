
def test_boxplot_tick_labels():
    # Test the `tick_labels` parameter.
    np.random.seed(19680801)
    data = np.random.random((10, 3))

    fig, ax = plt.subplots()
    ax.boxplot(data, tick_labels=['A', 'B', 'C'])
    assert [l.get_text() for l in ax.get_xticklabels()] == ['A', 'B', 'C']

