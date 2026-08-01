
def test_invalid_axis_limits():
    plt.plot([0, 1], [0, 1])
    with pytest.raises(ValueError):
        plt.xlim(np.nan)
    with pytest.raises(ValueError):
        plt.xlim(np.inf)
    with pytest.raises(ValueError):
        plt.ylim(np.nan)
    with pytest.raises(ValueError):
        plt.ylim(np.inf)

