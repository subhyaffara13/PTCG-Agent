
def test_big_decorators_horizontal():
    """Test that doesn't warn when xlabel too big."""
    fig, axs = plt.subplots(1, 2, figsize=(3, 2))
    axs[0].set_xlabel('a' * 30)
    axs[1].set_xlabel('b' * 30)

