
def test_boxplot_capwidths():
    data = np.random.rand(5, 3)
    fig, axs = plt.subplots(9)

    axs[0].boxplot(data, capwidths=[0.3, 0.2, 0.1], widths=[0.1, 0.2, 0.3])
    axs[1].boxplot(data, capwidths=[0.3, 0.2, 0.1], widths=0.2)
    axs[2].boxplot(data, capwidths=[0.3, 0.2, 0.1])

    axs[3].boxplot(data, capwidths=0.5, widths=[0.1, 0.2, 0.3])
    axs[4].boxplot(data, capwidths=0.5, widths=0.2)
    axs[5].boxplot(data, capwidths=0.5)

    axs[6].boxplot(data, widths=[0.1, 0.2, 0.3])
    axs[7].boxplot(data, widths=0.2)
    axs[8].boxplot(data)

