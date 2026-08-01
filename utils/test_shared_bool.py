
def test_shared_bool():
    with pytest.raises(TypeError):
        plt.subplot(sharex=True)
    with pytest.raises(TypeError):
        plt.subplot(sharey=True)

