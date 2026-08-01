
def test_spine_set_bounds_with_none():
    """Test that set_bounds(None, ...) uses original axis view limits."""
    fig, ax = plt.subplots()

    # Plot some data to set axis limits
    x = np.linspace(0, 10, 100)
    y = np.sin(x)
    ax.plot(x, y)

    xlim = ax.viewLim.intervalx
    ylim = ax.viewLim.intervaly
    # Use modified set_bounds with None
    ax.spines['bottom'].set_bounds(2, None)
    ax.spines['left'].set_bounds(None, None)

    # Check that get_bounds returns correct numeric values
    bottom_bound = ax.spines['bottom'].get_bounds()
    assert bottom_bound[1] is not None, "Higher bound should be numeric"
    assert np.isclose(bottom_bound[0], 2), "Lower bound should match provided value"
    assert np.isclose(bottom_bound[1],
                       xlim[1]), "Upper bound should match original value"

    left_bound = ax.spines['left'].get_bounds()
    assert (left_bound[0] is not None) and (left_bound[1] is not None), \
        "left bound should be numeric"
    assert np.isclose(left_bound[0], ylim[0]), "Lower bound should match original value"
    assert np.isclose(left_bound[1], ylim[1]), "Upper bound should match original value"

