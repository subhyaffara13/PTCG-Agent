
def test_annotate_across_transforms():
    x = np.linspace(0, 10, 200)
    y = np.exp(-x) * np.sin(x)

    fig, ax = plt.subplots(figsize=(3.39, 3))
    ax.plot(x, y)
    axins = ax.inset_axes([0.4, 0.5, 0.3, 0.3])
    axins.set_aspect(0.2)
    axins.xaxis.set_visible(False)
    axins.yaxis.set_visible(False)
    ax.annotate("", xy=(x[150], y[150]), xycoords=ax.transData,
                xytext=(1, 0), textcoords=axins.transAxes,
                arrowprops=dict(arrowstyle="->"))

