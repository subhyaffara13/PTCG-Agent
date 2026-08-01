
def test_legend_linewidth():
    """Test legend.linewidth parameter and rcParam."""
    fig, ax = plt.subplots()
    ax.plot([1, 2, 3], label='data')

    # Test direct parameter
    leg = ax.legend(linewidth=2.5)
    assert leg.legendPatch.get_linewidth() == 2.5

    # Test rcParam
    with mpl.rc_context({'legend.linewidth': 3.0}):
        fig, ax = plt.subplots()
        ax.plot([1, 2, 3], label='data')
        leg = ax.legend()
        assert leg.legendPatch.get_linewidth() == 3.0

    # Test None default (should inherit from patch.linewidth)
    with mpl.rc_context({'legend.linewidth': None, 'patch.linewidth': 1.5}):
        fig, ax = plt.subplots()
        ax.plot([1, 2, 3], label='data')
        leg = ax.legend()
        assert leg.legendPatch.get_linewidth() == 1.5

    # Test that direct parameter overrides rcParam
    with mpl.rc_context({'legend.linewidth': 1.0}):
        fig, ax = plt.subplots()
        ax.plot([1, 2, 3], label='data')
        leg = ax.legend(linewidth=4.0)
        assert leg.legendPatch.get_linewidth() == 4.0

