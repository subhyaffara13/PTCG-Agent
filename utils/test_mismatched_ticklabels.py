
def test_mismatched_ticklabels():
    fig, ax = plt.subplots()
    ax.plot(np.arange(10))
    ax.xaxis.set_ticks([1.5, 2.5])
    with pytest.raises(ValueError):
        ax.xaxis.set_ticklabels(['a', 'b', 'c'])

