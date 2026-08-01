
def test_pie_invalid_labels():
    # Test ValueError raised when feeding short labels list to axes.pie
    fig, ax = plt.subplots()
    with pytest.raises(ValueError):
        ax.pie([1, 2, 3], labels=["One", "Two"])

