
def test_pie_all_zeros():
    fig, ax = plt.subplots()
    with pytest.raises(ValueError, match="All wedge sizes are zero"):
        ax.pie([0, 0], labels=["A", "B"])

