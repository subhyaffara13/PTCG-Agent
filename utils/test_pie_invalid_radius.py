
def test_pie_invalid_radius():
    # Test ValueError raised when feeding negative radius to axes.pie
    fig, ax = plt.subplots()
    with pytest.raises(ValueError):
        ax.pie([1, 2, 3], radius=-5)

