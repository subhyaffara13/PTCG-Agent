
def test_labels_first():
    # test labels to left of markers
    fig, ax = plt.subplots()
    ax.plot(np.arange(10), '-o', label=1)
    ax.plot(np.ones(10)*5, ':x', label="x")
    ax.plot(np.arange(20, 10, -1), 'd', label="diamond")
    ax.legend(loc='best', markerfirst=False)

