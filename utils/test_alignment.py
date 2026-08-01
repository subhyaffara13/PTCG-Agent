
def test_alignment():
    plt.figure()
    ax = plt.subplot(1, 1, 1)

    x = 0.1
    for rotation in (0, 30):
        for alignment in ('top', 'bottom', 'baseline', 'center'):
            ax.text(
                x, 0.5, alignment + " Tj", va=alignment, rotation=rotation,
                bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))
            ax.text(
                x, 1.0, r'$\sum_{i=0}^{j}$', va=alignment, rotation=rotation)
            x += 0.1

    ax.plot([0, 1], [0.5, 0.5])
    ax.plot([0, 1], [1.0, 1.0])

    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1.5)
    ax.set_xticks([])
    ax.set_yticks([])

