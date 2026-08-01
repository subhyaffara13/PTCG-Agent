
def test_big_decorators_vertical():
    """Test that doesn't warn when ylabel too big."""
    fig, axs = plt.subplots(2, 1, figsize=(3, 2))
    axs[0].set_ylabel('a' * 20)
    axs[1].set_ylabel('b' * 20)

