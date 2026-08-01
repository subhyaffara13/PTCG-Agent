
def test_pie_invalid_explode():
    # Test ValueError raised when feeding short explode list to axes.pie
    fig, ax = plt.subplots()
    with pytest.raises(ValueError):
        ax.pie([1, 2, 3], explode=[0.1, 0.1])

