
def test_boxplot_custom_capwidths():

    x = np.linspace(-7, 7, 140)
    x = np.hstack([-25, x, 25])
    fig, ax = plt.subplots()

    ax.boxplot([x, x], notch=1, capwidths=[0.01, 0.2])

