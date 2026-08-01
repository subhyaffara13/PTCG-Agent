
def test_imshow_10_10_5():
    fig, ax = plt.subplots()
    arr = np.arange(500).reshape((10, 10, 5))
    with pytest.raises(TypeError):
        ax.imshow(arr)

