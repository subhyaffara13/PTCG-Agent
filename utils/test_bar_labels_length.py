
def test_bar_labels_length():
    _, ax = plt.subplots()
    with pytest.raises(ValueError):
        ax.bar(["x", "y"], [1, 2], label=["X", "Y", "Z"])
    _, ax = plt.subplots()
    with pytest.raises(ValueError):
        ax.bar(["x", "y"], [1, 2], label=["X"])

