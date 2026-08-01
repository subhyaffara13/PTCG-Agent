
def test_violin_point_mass():
    """Violin plot should handle point mass pdf gracefully."""
    plt.violinplot(np.array([0, 0]))

