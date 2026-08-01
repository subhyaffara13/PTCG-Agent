
def test_subplots_reuse_existing_figure_error():
    """Test interaction of plt.subplots(num=...) with existing figures."""
    # Create a figure with a specific number first.
    fig = plt.figure(1)

    # Case 1: Reusing without clear=True should raise ValueError
    with pytest.raises(ValueError, match="already exists"):
        plt.subplots(num=1)

    # Case 2: Reusing WITH clear=True should work fine (no error)
    fig_new, axs = plt.subplots(num=1, clear=True)
    assert fig_new is fig

    # Case 3: Test passing the actual Figure object (The "Narrow Check")
    with pytest.raises(ValueError, match="cannot be a FigureBase instance"):
        plt.subplots(num=fig)

    plt.close(1)

