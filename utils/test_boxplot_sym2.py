
def test_boxplot_sym2():
    # Randomness used for bootstrapping.
    np.random.seed(937)

    x = np.linspace(-7, 7, 140)
    x = np.hstack([-25, x, 25])
    fig, [ax1, ax2] = plt.subplots(1, 2)

    ax1.boxplot([x, x], bootstrap=10000, sym='^')
    ax1.set_ylim(-30, 30)

    ax2.boxplot([x, x], bootstrap=10000, sym='g')
    ax2.set_ylim(-30, 30)

