
def test_nanscatter():
    fig, ax = plt.subplots()

    h = ax.scatter([np.nan], [np.nan], marker="o",
                   facecolor="r", edgecolor="r", s=3)

    ax.legend([h], ["scatter"])

    fig, ax = plt.subplots()
    for color in ['red', 'green', 'blue']:
        n = 750
        x, y = np.random.rand(2, n)
        scale = 200.0 * np.random.rand(n)
        ax.scatter(x, y, c=color, s=scale, label=color,
                   alpha=0.3, edgecolors='none')

    ax.legend()
    ax.grid(True)

