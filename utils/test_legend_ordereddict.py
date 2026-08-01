
def test_legend_ordereddict():
    # smoketest that ordereddict inputs work...

    X = np.random.randn(10)
    Y = np.random.randn(10)
    labels = ['a'] * 5 + ['b'] * 5
    colors = ['r'] * 5 + ['g'] * 5

    fig, ax = plt.subplots()
    for x, y, label, color in zip(X, Y, labels, colors):
        ax.scatter(x, y, label=label, c=color)

    handles, labels = ax.get_legend_handles_labels()
    legend = collections.OrderedDict(zip(labels, handles))
    ax.legend(legend.values(), legend.keys(),
              loc='center left', bbox_to_anchor=(1, .5))

