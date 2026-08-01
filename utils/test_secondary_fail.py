
def test_secondary_fail():
    fig, ax = plt.subplots()
    ax.plot(np.arange(2, 11), np.arange(2, 11))
    with pytest.raises(ValueError):
        ax.secondary_xaxis(0.2, functions=(lambda x: 1 / x))
    with pytest.raises(ValueError):
        ax.secondary_xaxis('right')
    with pytest.raises(ValueError):
        ax.secondary_yaxis('bottom')
    with pytest.raises(TypeError):
        ax.secondary_xaxis(0.2, transform='error')

