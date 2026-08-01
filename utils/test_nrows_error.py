
def test_nrows_error():
    with pytest.raises(TypeError):
        plt.subplot(nrows=1)
    with pytest.raises(TypeError):
        plt.subplot(ncols=1)

