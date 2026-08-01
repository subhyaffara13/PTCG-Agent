
def test_violinplot_empty_dataset():
    fig, ax = plt.subplots()
    # This should not raise an exception
    parts = ax.violinplot([np.random.randn(100), [], [np.nan, np.nan]])
    assert len(parts["bodies"]) == 3

