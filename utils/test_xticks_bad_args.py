
def test_xticks_bad_args():
    ax = plt.figure().add_subplot()
    with pytest.raises(TypeError, match='must be a sequence'):
        ax.set_xticks([2, 9], 3.1)
    with pytest.raises(TypeError, match='must be a sequence'):
        ax.set_xticks([2, 9], ax)
    with pytest.raises(ValueError, match='must be 1D'):
        plt.xticks(np.arange(4).reshape((-1, 1)))
    with pytest.raises(ValueError, match='must be 1D'):
        plt.xticks(np.arange(4).reshape((1, -1)))
    with pytest.raises(ValueError, match='must be 1D'):
        plt.xticks(np.arange(4).reshape((-1, 1)), labels=range(4))
    with pytest.raises(ValueError, match='must be 1D'):
        plt.xticks(np.arange(4).reshape((1, -1)), labels=range(4))

