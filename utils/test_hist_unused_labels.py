
def test_hist_unused_labels():
    # When a list with one dataset and N elements is provided and N labels, ensure
    # that the first label is used for the dataset and all other labels are ignored
    fig, ax = plt.subplots()
    ax.hist([[1, 2, 3]], label=["values", "unused", "also unused"])
    _, labels = ax.get_legend_handles_labels()
    assert labels == ["values"]

