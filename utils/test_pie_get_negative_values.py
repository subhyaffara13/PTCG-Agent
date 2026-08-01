
def test_pie_get_negative_values():
    # Test the ValueError raised when feeding negative values into axes.pie
    fig, ax = plt.subplots()
    with pytest.raises(ValueError):
        ax.pie([5, 5, -3], explode=[0, .1, .2])

